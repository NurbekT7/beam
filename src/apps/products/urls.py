from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ProductViewSet, CategoriesView

router = SimpleRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("categories/", CategoriesView.as_view()),
    path("categories/<int:cat_id>/sub/", CategoriesView.as_view()),
]