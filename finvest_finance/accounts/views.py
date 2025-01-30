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

from accounts.models import Portfolio, Transaction
from .serializers import (
    PortfolioSerializer,
    TransactionSerializer,
)
import boto3
from django.conf import settings


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
            stock = get_object_or_404(Stock, stock_symbol=stock_symbol)

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
            f"{instance.id}/{field_name}/{file.name}"  # Customize as needed
        )
        s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, s3_file_name)

        # Construct the S3 file URL
        s3_file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{s3_file_name}"
        return s3_file_url
