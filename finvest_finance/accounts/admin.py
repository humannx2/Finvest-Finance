from django.contrib import admin
from . models import Portfolio, CustomUser

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'stock_name', 'quantity', 'purchase_price', 'date_of_purchase')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_verified', 'demat_account', 'pan_card_provided', 'pan_card_number')

