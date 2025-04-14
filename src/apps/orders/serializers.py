from rest_framework import serializers
from apps.orders.models import Order, OrderedProduct
from apps.products.models import Product
from django.db import transaction
from django.core.exceptions import ValidationError
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json


class OrderedProductSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderedProduct
        fields = ['id', 'product', 'product_id', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderedProductSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'total_price', 'products']

    def validate(self, attrs):
        products_data = self.initial_data.get('products', [])
        errors = []
        for item in products_data:
            try:
                product = Product.objects.get(id=item['product_id'])
                if product.quantity < int(item['quantity']):
                    errors.append(f"Недостаточно товара '{product.name}' — в наличии {product.quantity}, запрошено {item['quantity']}")
            except Product.DoesNotExist:
                errors.append(f"Продукт с id={item['product_id']} не найден.")
        if errors:
            raise serializers.ValidationError({'products': errors})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)

        total = 0
        for item in products_data:
            product = item['product']
            quantity = item['quantity']

            if product.quantity < quantity:
                raise ValidationError(f"Недостаточно товара '{product.name}'")

            product.quantity -= quantity
            product.save()

            OrderedProduct.objects.create(order=order, product=product, quantity=quantity)
            total += product.price * quantity

        order.total_price = total
        order.save()

        products_list = []
        for p in order.products.select_related('product'):
            products_list.append({
                "id": p.product.id if p.product else None,
                "name": p.product.name if p.product else "deleted product",
                "quantity": p.quantity
            })

        data = {
            "id": order.id,
            "email": order.user.email if order.user else None,
            "name": f"{order.user.first_name} {order.user.last_name}" if order.user else "Гость",
            "total_price": float(order.total_price),
            "created_at": order.created_at.isoformat(),
            "products": products_list
        }

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "orders",
            {
                "type": "order_message",
                "message": json.dumps(data)
            }
        )

        return order
