from django.db import models
from smart_selects.db_fields import GroupedForeignKey


class Category(models.Model):
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=150)
    img = models.ImageField(upload_to="products/cat/")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Category"


class SubCategory(models.Model):
    is_active = models.BooleanField(default=False)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sub_categories")
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sub category"


class Product(models.Model):
    is_active = models.BooleanField(default=False)
    cat = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, editable=False)
    sub_cat = GroupedForeignKey(SubCategory, "cat", null=True, blank=True, limit_choices_to={"is_active": True})

    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.sub_cat:
            self.cat = self.sub_cat.cat
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-is_active', '-id']


class ProductImg(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='product_img')
    img = models.ImageField(upload_to="products/product/%Y_%m", blank=True, null=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
