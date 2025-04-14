from django.contrib import admin
from .models import Order, OrderedProduct

class OrderedProductInline(admin.TabularInline):
    model = OrderedProduct
    extra = 0
    readonly_fields = ('product', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created_at')
    inlines = [OrderedProductInline]