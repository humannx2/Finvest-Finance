from django.urls import path, include
from accounts.views import OrderView
from rest_framework.routers import DefaultRouter
from accounts.views import (
    PortfolioViewSet,
    TransactionViewSet,
    ProfileViewSet,
    login_view,
    logout_view,
    register,
    cta_form_view,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
)  # ,TokenObtainPairView

router = DefaultRouter()
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register, name="register"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('order/', OrderView.as_view(), name='order'),
    path('contact-us/', cta_form_view, name='contact-us'),
    path('', include(router.urls)),
]
