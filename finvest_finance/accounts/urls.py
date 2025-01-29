from django.urls import path
from .views import OrderConfirmationView

urlpatterns = [
    path('order/', OrderConfirmationView.as_view(), name='order'),
]
