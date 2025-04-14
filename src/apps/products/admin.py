from django.contrib import admin
from django.utils.html import mark_safe
from apps.products.models import (
    Category,
    SubCategory,
    Product,
    ProductImg,
)

from django.contrib.auth.models import Group

admin.site.unregister(Group)

try:
    from rest_framework.authtoken.models import TokenProxy as DRFToken
except ImportError:
    from rest_framework.authtoken.models import Token as DRFToken

admin.site.unregister(DRFToken)


class SubCategoryInline(admin.StackedInline):
    model = SubCategory
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "is_active", "name", "get_img")
    list_editable = ("is_active",)
    list_display_links = ("id", "name")

    inlines = (SubCategoryInline,)

    def get_img(self, object):
        if object.img:
            return mark_safe(f"<img src='{object.img.url}' height='60'>")
        return 'BEAM?'


class ProductImgInline(admin.TabularInline):
    model = ProductImg
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "is_active", "name", "sub_cat", "get_img")
    list_editable = ("is_active",)
    list_display_links = ("id", "name")
    search_fields = ("id", "name", 'price')
    list_filter = ["cat", "sub_cat", ]

    inlines = (ProductImgInline,)

    def get_img(self, object):
        if object.product_img.first():
            return mark_safe(f"<img src='{object.product_img.first().img.url}' height='60'>")
        return 'BEAM?'
