from django.urls import path, include
from .views import OrderConfirmationView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('order/', OrderConfirmationView.as_view(), name='order'),
]
