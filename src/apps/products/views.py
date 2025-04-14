from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Q

from .filters import ProductFilter

from apps.products.models import (
    Category,
    SubCategory,
    Product,
    ProductImg,
)
from apps.products.serializers import (
    ProductImgSerializer,
    ProductSerializer,
    SubCategorySerializer,
    CategorySerializer,
)


class CategoriesView(generics.ListAPIView):
    def get_queryset(self):
        cat_id = self.kwargs.get("cat_id")

        if cat_id is not None:
            return SubCategory.objects.filter(is_active=True, cat_id=cat_id)
        return Category.objects.prefetch_related("sub_categories").order_by("id").filter(is_active=True)

    def get_serializer_class(self):
        if self.kwargs.get("cat_id") is not None:
            return SubCategorySerializer
        return CategorySerializer


class ProductViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Product.objects.select_related("cat", "sub_cat")
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'cat__name', 'sub_cat__name']

    def get_serializer_class(self):
        return ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)

        ordering = self.request.query_params.get("ordering", "-id")
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
