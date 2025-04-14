# import time
#
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Order
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# import json
# import time
#
# @receiver(post_save, sender=Order)
# def send_order_created_ws(sender, instance, created, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#
#         products = []
#         for item in instance.products.select_related('product'):
#             products.append({
#                 'id': item.product.id if item.product else None,
#                 'title': item.product.title if item.product else 'Item deleted',
#                 'quantity': item.quantity
#             })
#
#         data = {
#             'id': instance.id,
#             'email': instance.user.email if instance.user else None,
#             'name': f"{instance.user.first_name} {instance.user.last_name}" if instance.user else "Гость",
#             'total_price': instance.total_price,
#             'created_at': instance.created_at.isoformat(),
#             'products': products
#         }
#
#         async_to_sync(channel_layer.group_send)(
#             "orders",
#             {
#                 "type": "order_message",
#                 "message": json.dumps(data)
#             }
#         )
