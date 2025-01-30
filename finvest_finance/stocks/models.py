from django.db import models


class Stock(models.Model):
    isin = models.CharField(
        max_length=12, unique=True
    )  # International Securities Identification Number
    stock_name = models.CharField(max_length=255)  # Name of the stock
    stock_symbol = models.CharField(max_length=10)  # Stock symbol (Ticker)
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stock({self.isin})"


class StockValue(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=16, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
