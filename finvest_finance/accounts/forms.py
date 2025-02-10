from django import forms
from accounts.models import Stock, Profile


class OrderForm(forms.Form):
    stock_symbol = forms.CharField(max_length=10)
    order_type = forms.ChoiceField(
        choices=[('Buy', 'Buy'), ('Sell', 'Sell')], initial='Buy'
    )
    qty = forms.IntegerField(min_value=1, initial=100)
    price = forms.FloatField(min_value=0.01, initial=1500)

    def clean_stock_symbol(self):
        stock_symbol = self.cleaned_data['stock_symbol']
        if not Stock.objects.filter(stock_symbol=stock_symbol).exists():
            raise forms.ValidationError(
                f"Stock symbol {stock_symbol} does not exist."
            )
        return stock_symbol

    def clean_qty(self):
        qty = self.cleaned_data['qty']
        if qty <= 0:
            raise forms.ValidationError("Quantity must be a positive integer.")
        return qty

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be a positive value.")
        return price


class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'phone_number', 'dob')


class CTAForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    message = forms.CharField(widget=forms.Textarea, required=True)
