from rest_framework import serializers
from apps.products.models import (
    Category,
    SubCategory,
    Product,
    ProductImg,
)


class ProductImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImg
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    product_img = ProductImgSerializer(many=True)
    main_img = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_main_img(self, obj):
        if obj.product_img.first():
            return obj.product_img.first().img.url
        return None


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
