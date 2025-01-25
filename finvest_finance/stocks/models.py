from django.db import models

class StockData(models.Model):
    ISIN = models.CharField(max_length=12, unique=True)  # International Securities Identification Number
    FaceValue = models.DecimalField(max_digits=15, decimal_places=2)  # Face value of the stock
    TotalShare = models.DecimalField(max_digits=20, decimal_places=2)  # Total shares in circulation
    TotalIncome = models.DecimalField(max_digits=20, decimal_places=2)  # Total income
    ProfileAfterTax = models.DecimalField(max_digits=20, decimal_places=2)  # Profile after tax
    EPS = models.DecimalField(max_digits=20, decimal_places=2)  # Earnings per share
    PE = models.DecimalField(max_digits=20, decimal_places=2)  # Price-to-earnings ratio
    PB = models.DecimalField(max_digits=20, decimal_places=2)  # Price-to-book ratio
    MarketCapitalization = models.DecimalField(max_digits=20, decimal_places=2)  # Market Cap
    EnterpriseValue = models.DecimalField(max_digits=20, decimal_places=2)  # Enterprise Value
    BookValue = models.DecimalField(max_digits=20, decimal_places=2)  # Book Value
    IntrinsicValue = models.DecimalField(max_digits=20, decimal_places=2)  # Intrinsic Value
    EarningYields = models.DecimalField(max_digits=20, decimal_places=2)  # Earning Yield
    Sector = models.CharField(max_length=255)  # Sector (String)
    SubSector = models.CharField(max_length=255)  # Sub-Sector (String)
    Category = models.CharField(max_length=255)  # Category (String)
    CashflowOperation = models.DecimalField(max_digits=20, decimal_places=2)  # Cashflow from Operations
    CashflowFinancing = models.DecimalField(max_digits=20, decimal_places=2)  # Cashflow from Financing
    AverageTradedPrice = models.DecimalField(max_digits=20, decimal_places=2)  # Average traded price

    def __str__(self):
        return f"StockData({self.ISIN})"
