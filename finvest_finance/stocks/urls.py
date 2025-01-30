from django.urls import path, include
router = DefaultRouter()

from rest_framework.routers import DefaultRouter
from .views import StockViewSet, StockValueViewSet

router = DefaultRouter()
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'stock-values', StockValueViewSet, basename='stock-value')



urlpatterns = [
    path(
        '', include(router.urls)
    ),  # Automatically includes routes for CRUD operations
]
