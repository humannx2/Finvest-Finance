from django.urls import path, include
from .views import OrderConfirmationView


from rest_framework.routers import DefaultRouter
from .views import (
    StockViewSet,
    StockValueViewSet,
    PortfolioViewSet,
    TransactionViewSet,
)

router = DefaultRouter()
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'stock-values', StockValueViewSet, basename='stock-value')
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('order/', OrderConfirmationView.as_view(), name='order'),
]
