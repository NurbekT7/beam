from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # main
    path('admin/', admin.site.urls),

    path('api/', include("apps.accounts.urls")),
    path('api/', include("apps.products.urls")),
    path('api/', include("apps.orders.urls")),

    # swagger
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema')),
] + static('/static/', document_root = settings.STATIC_ROOT) + static('/media/', document_root = settings.MEDIA_ROOT)