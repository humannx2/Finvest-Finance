from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from stocks.models import StockData

User = get_user_model()

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')  # Reference to the User model
    stock = models.ForeignKey(StockData, on_delete=models.CASCADE, related_name='portfolios')  # ForeignKey to StockData
    quantity = models.PositiveIntegerField()  # Quantity of the stock owned
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at which the stock was purchased
    date_of_purchase = models.DateField()  # Date of purchase

    def __str__(self):
        return f"{self.stock_name.stock_name} - {self.user.username}"  # Display stock name and username



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
