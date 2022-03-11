from api import views
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
# from rest_framework_nested import routers

router = DefaultRouter()
router.register(r'promo', views.PromoViewSet, basename='promo')

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', include(router.urls)),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]