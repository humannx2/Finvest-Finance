from django.db import models
from datetime import date


class Stock(models.Model):
    isin = models.CharField(
        max_length=12, unique=True
    )  # International Securities Identification Number
    stock_name = models.CharField(max_length=255)  # Name of the stock
    stock_symbol = models.CharField(max_length=10)  # Stock symbol (Ticker)
    company_logo = models.URLField(
        default="https://cdn.logo.com/hotlink-ok/logo-social.png"
    )
    face_value = models.DecimalField(
        max_digits=15, decimal_places=2
    )  # Face value of the stock
    total_share = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # Total shares in circulation
    total_income = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # Total income
    profile_after_tax = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # Profile after tax
    eps = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # Earnings per share
    pe = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # Price-to-earnings ratio
    pb = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # Price-to-book ratio
    market_capitalization = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # Market Cap
    enterprise_value = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # Enterprise Value
    book_value = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # Book Value
    intrinsic_value = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # Intrinsic Value
    earning_yields = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # Earning Yield
    sector = models.CharField(max_length=255)  # Sector (String)
    sub_sector = models.CharField(max_length=255)  # Sub-Sector (String)
    category = models.CharField(max_length=255)  # Category (String)
    cashflow_operation = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # Cashflow from Operations
    cashflow_financing = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # Cashflow from Financing
    average_traded_price = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # Average traded price

    lot_size = models.DecimalField(max_digits=20, decimal_places=2)
    legal_name = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    popular = models.BooleanField(default=False)
    exclusive = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    top_pick = models.BooleanField(default=False)

    about = models.TextField(blank=True)

    def __str__(self):
        return f"Stock({self.isin})"


# publish/ unpublish , exclusive, r
# pan card, cancelled cheque, user demat w/ cml copy (w/ sorting)
# reg date, name email , pan card, demat, total invested
# transactions:- verified filter and sorted, validatio- verification_pending, confirmed, cancelled


class StockValue(models.Model):
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name='stock_values'
    )
    value = models.DecimalField(max_digits=16, decimal_places=2)
    date = models.DateField(
        default=date.today
    )  # Sets the default date to today

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
