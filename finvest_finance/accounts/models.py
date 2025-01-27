from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

User = get_user_model()

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    stock_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_purchase = models.DateField()

    def __str__(self):
        return f"{self.stock_name} - {self.user.username}"


class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)  # Whether the user is verified
    demat_account = models.CharField(max_length=20, unique=True, blank=False)  # Demat Account Number
    pan_card_provided = models.BooleanField(default=False)  # If PAN card is uploaded
    pan_card_number = models.CharField(max_length=10, unique=True, blank=True, null=True)  # Optional PAN card number

    # Specify related_name to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Prevents clashes with auth.User.groups
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Prevents clashes with auth.User.user_permissions
        blank=True,
    )

    def __str__(self):
        return self.username
