from django.shortcuts import render
from django.views import View
from datetime import date
from django.contrib.auth.models import User  # Assuming using Django's default User model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Apply the login_required decorator to ensure the view is accessible only by authenticated users
@method_decorator(login_required, name='dispatch')
class OrderView(View):
    def post(self, request, *args, **kwargs):
        # Retrieve the authenticated user's name
        user = request.user
        # Context data for rendering the email template
        context = {
            'user_name': user.name,  # Use the user_name from the authenticated user
            'share_name': request.POST.get('share_name', 'ABC Corp'),
            'order_date': date.today(),
            'order_type': request.POST.get('order_type', 'Buy'),
            'qty': int(request.POST.get('qty', 100)),  # Default qty if not provided
            'price': float(request.POST.get('price', 1500)),
            'total_amount': float(request.POST.get('price', 1500)) * int(request.POST.get('qty', 100)),
            'total_investment': float(request.POST.get('price', 1500)) * int(request.POST.get('qty', 100)),
            'whatsapp_link': 'https://wa.me/1234567890',
            'website_url': 'https://www.faanfinvest.com',
            'unsubscribe_link': '#',
            'logo_url': 'https://example.com/logo.png',
        }
        
        # Render the template with the context
        return render(request, 'order_confirmation_template.html', context)
