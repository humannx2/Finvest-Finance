from django.contrib import admin
from .models import Portfolio, Profile


# @admin.register(Portfolio)
# class PortfolioAdmin(admin.ModelAdmin):
#     list_display = (
#         'user',
#         'stock',
#         'quantity',
#         'purchase_price',
#         'date_of_purchase',
#     )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'is_verified',
        'demat_account',
        'pan_card_validated',
        'pan_card_number',
    )
