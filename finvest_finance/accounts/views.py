from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import Stock
from datetime import date
from accounts.forms import OrderForm
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets

from accounts.models import Portfolio, Transaction, Profile
from .serializers import (
    PortfolioSerializer,
    TransactionSerializer,
    ProfileSerializer,
)
import boto3
from django.conf import settings

import random
import string
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view

from django.contrib.auth.tokens import (
    PasswordResetTokenGenerator,
)

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

from accounts.forms import CustomerRegistrationForm
from accounts.models import Profile as Customer
from accounts.serializers import ProfileSerializer as CustomerSerializer


from django.core.mail import send_mail
from .forms import CTAForm
from django.http import HttpResponse
from django.template.loader import render_to_string


User = get_user_model()

default_token_generator = PasswordResetTokenGenerator()


def generate_username(email):
    # Generate a username based on the email and a random number
    username_base = email.split("@")[0]
    # Use the part before the '@' as the base
    random_suffix = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=4)
    )
    return f"{username_base}_{random_suffix}"


@api_view(["POST"])
def register(request):
    email = request.data.get("email")
    password = request.data.get("password")

    # Validate email and password presence
    if not (email and password):
        return Response(
            {"message": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        if User.objects.filter(email=email).first():
            return Response(
                {"detail": "User already exists. Please log in."},
                status=status.HTTP_409_CONFLICT,
            )

        user = User.objects.create_user(
            username=generate_username(email), password=password, email=email
        )
    except Exception as e:
        return Response(
            {"message": f"Error creating user: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Process customer registration form
    form = CustomerRegistrationForm({"user": user, **request.data})
    if form.is_valid():
        customer = form.save(commit=False)
        # customer.user = user
        customer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Customer registration successfull.",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response(
            {"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@csrf_exempt
@api_view(["POST"])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, username=user.username, password=password)

    if user is not None:
        login(request, user)
        refresh = RefreshToken.for_user(user)

        try:
            customer = Customer.objects.get(user=user)

            return Response(
                {
                    "customer": CustomerSerializer(customer).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        except Customer.DoesNotExist:
            return Response(
                {"message": "User is not a customer"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"message": "Login successful", "csrf_token": get_token(request)},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


@csrf_exempt
@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


@method_decorator(login_required, name='dispatch')
class OrderView(View):
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)

        if form.is_valid():
            # Retrieve the authenticated user's name
            user: User = request.user
            # Get stock data
            stock_symbol = form.cleaned_data['stock_symbol']
            # order_type = form.cleaned_data['order_type']
            # qty = form.cleaned_data['qty']
            # price = form.cleaned_data['price']
            stock = get_object_or_404(Stock, stock_symbol=stock_symbol)

            # Context data for rendering the email template
            context = {
                'user_name': getattr(
                    user, "first_name", ""
                ),  # Use the user_name from the authenticated user
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


# Portfolio ViewSet
class PortfolioViewSet(viewsets.ModelViewSet):
    """ViewSet for handling CRUD operations for Portfolio."""

    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


# Transaction ViewSet
class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for handling CRUD operations for Transaction."""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Process the data for URL fields and file uploads
        instance = self.perform_uploads(serializer.validated_data)

        # Save the instance
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)

        # Process the data for URL fields and file uploads
        updated_instance = self.perform_uploads(
            serializer.validated_data, instance
        )

        # Save the instance
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_uploads(self, validated_data, instance=None):
        # If instance is None, we are creating a new object
        if instance is None:
            instance = Transaction

        for field_name, file in self.validated_data.items():
            if isinstance(file, str) and file.startswith('http'):
                # Skip if it's already a URL
                continue

            if hasattr(instance, field_name) and isinstance(file, bytes):
                # Upload the file to S3
                s3_file_url = self.upload_to_s3(file, field_name, instance)
                setattr(instance, field_name, s3_file_url)

        # Save the instance with updated file URLs
        instance.save()
        return instance

    def upload_to_s3(self, file, field_name, instance):
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        # Define the S3 file name and upload
        s3_file_name = (
            f"/profiles/{instance.id}/{field_name}"  # Customize as needed
        )
        s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, s3_file_name)

        # Construct the S3 file URL
        s3_file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{s3_file_name}"
        return s3_file_url


def cta_form_view(request):
    if request.method == 'POST':
        form = CTAForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Email content for the admin
            subject = "New CTA Form Submission"
            email_body = render_to_string(
                "contact_us.html", {**form.cleaned_data}
            )
            # Send email to the admin
            send_mail(
                subject,
                email_body,
                email,  # Sender's email (the visitor's email)
                [settings.ADMIN_EMAIL],  # Recipient email (admin's email)
                fail_silently=False,
            )

            return HttpResponse('Thank you for your submission!')
        else:
            return render(
                request,
                'cta_form.html',
                {'form': form, 'error': 'Invalid form data!'},
            )

    # If GET request, display empty form
    else:
        form = CTAForm()

    return render(request, 'cta_form.html', {'form': form})


# Profile ViewSet
class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for handling CRUD operations for Portfolio."""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = Profile.objects.all()
        sort_by = self.request.query_params.get('sort_by', None)
        
        if sort_by:
            # Map frontend sort parameters to model fields
            sort_mapping = {
                'registration_date': 'created_at',  # Assuming your date field is called created_at
                'name': 'user__first_name',  # Assuming name is in the related User model
                'total_investment': 'total_investment'
            }
            
            # Get the corresponding model field
            sort_field = sort_mapping.get(sort_by)
            
            # Check if descending order is requested
            order = self.request.query_params.get('order', 'asc')
            if order == 'desc':
                sort_field = f'-{sort_field}'
                
            if sort_field:
                queryset = queryset.order_by(sort_field)
        
        return queryset