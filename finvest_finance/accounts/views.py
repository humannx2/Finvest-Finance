from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms
from .models import StockData
from datetime import date
from accounts.forms import OrderForm
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


@method_decorator(login_required, name='dispatch')
class OrderView(View):
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)

        if form.is_valid():
            # Retrieve the authenticated user's name
            user = request.user
            # Get stock data
            stock_symbol = form.cleaned_data['stock_symbol']
            # order_type = form.cleaned_data['order_type']
            # qty = form.cleaned_data['qty']
            # price = form.cleaned_data['price']
            stock = get_object_or_404(StockData, stock_symbol=stock_symbol)

            # Context data for rendering the email template
            context = {
                'user_name': user.name,  # Use the user_name from the authenticated user
                'share_name': stock.stock_name,
                'order_date': date.today(),
                'order_type': form.cleaned_data['order_type'],
                'qty': form.cleaned_data['qty'],
                'price': form.cleaned_data['price'],
                'total_amount': form.cleaned_data['price']
                * form.cleaned_data['qty'],
                'total_investment': form.cleaned_data['price']
                * form.cleaned_data['qty'],
                'whatsapp_link': 'https://wa.me/8377081003',
                'website_url': 'https://www.faanfinvest.com',
                'unsubscribe_link': '#',
                'logo_url': 'https://example.com/logo.png',
            }

            # Render the template with the context
            return render(request, 'order_confirmation_template.html', context)
        else:
            # Return errors if form is not valid
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
