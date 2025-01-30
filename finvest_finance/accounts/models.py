from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from stocks.models import Stock

User = get_user_model()


class Portfolio(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='portfolios', null=True
    )  # Reference to the User model
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name='portfolios'
    )  # ForeignKey to Stock
    quantity = models.PositiveIntegerField()  # Quantity of the stock owned
    purchase_price = models.DecimalField(
        max_digits=16, decimal_places=4
    )  # Price at which the stock was purchased
    date_of_purchase = models.DateField(blank=True)  # Date of purchase

    def __str__(self):
        return f"{self.stock_name.stock_name} - {self.user.username}"  # Display stock name and username


class Transaction(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='portfolios', null=True
    )  # Reference to the User model
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name='portfolios'
    )  # ForeignKey to Stock
    quantity = (
        models.PositiveIntegerField()
    )  # Quantity of the stock bought or sold
    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Price at
    date_of_transaction = models.DateField(blank=True)  # Date of transaction
    transaction_type = models.CharField(max_length=4, choices=[('buy', 'sell')])
    payment_id = models.CharField(max_length=64)
    payment_screenshot = models.URLField()
    is_valid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CustomUser(AbstractUser):
    name = models.CharField(max_length=32, default="Enter your name")
    email = models.EmailField(unique=True, default="Enter your email")
    dob = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(
        default=False
    )  # Whether the user is verified
    demat_account = models.CharField(
        max_length=20, unique=True, blank=False
    )  # Demat Account Number
    pan_card_provided = models.BooleanField(
        default=False
    )  # If PAN card is uploaded
    pan_card_number = models.CharField(
        max_length=10, unique=True, blank=True, null=True
    )
    pan_card_image = models.URLField(
        default="https://miro.medium.com/v2/resize:fit:1358/1*xMy-08e9N2DuFlhxuWO_sw.jpeg"
    )
    aadhar_card_image = models.URLField(
        default="https://1.bp.blogspot.com/-jwvQnOCuftw/Xx2KtXfa-NI/AAAAAAAAECs/kJF4B2rSx8ED3qF9g4Puhf7EDL3p6t_5wCLcBGAsYHQ/s2048/aadhar.png"
    )
    bank_statement_image = models.URLField(
        default="https://admeonline.com/wp-content/uploads/2018/07/How-to-get-SBI-account-statement_online-using-internet-banking.png"
    )

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
