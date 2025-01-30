from django.urls import path, include
from .views import OrderView
from rest_framework.routers import DefaultRouter
from .views import (
    # StockViewSet,
    # StockValueViewSet,
    PortfolioViewSet,
    TransactionViewSet,
)
from .views import (
    login_view,
    logout_view,
    register,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
)  # ,TokenObtainPairView

router = DefaultRouter()
# router.register(r'stocks', StockViewSet, basename='stock')
# router.register(r'stock-values', StockValueViewSet, basename='stock-value')
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register, name="register"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('order/', OrderView.as_view(), name='order'),
    path('', include(router.urls)),
]
