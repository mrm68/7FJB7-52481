from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('reservation.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/documentation/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/documentation/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui-home'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/accounts/', include('accounts.urls')),
]
