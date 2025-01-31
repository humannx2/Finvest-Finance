from django.template.loader import render_to_string
from django.core.mail import send_mail

def send_welcome_email(user_name, email, order_details, whatsapp_link, website_url, logo_url, unsubscribe_link):
    # Sample data for order details
    context = {
        "user_name": user_name,
        "share_name": order_details.get("share_name"),
        "order_date": order_details.get("order_date"),
        "order_type": order_details.get("order_type"),
        "qty": order_details.get("qty"),
        "price": order_details.get("price"),
        "total_amount": order_details.get("total_amount"),
        "whatsapp_link": whatsapp_link,
        "website_url": website_url,
        "logo_url": logo_url,
        "unsubscribe_link": unsubscribe_link,
    }
    
    # Render the email template
    email_body = render_to_string("finvest_finance/accounts/templates/welcome.html", context)
    
    # Send the email
    send_mail(
        subject="Welcome to Faang Finvest Private Limited",
        message="",
        html_message=email_body,
        from_email="noreply@faanfinvest.com",
        recipient_list=[email],
        fail_silently=False,
    )


def send_share_purchase_email(user_name, email, order_details, bank_details, whatsapp_link, website_url, logo_url, unsubscribe_link):
    # Context for email template
    context = {
        "user_name": user_name,
        "share_name": order_details.get("share_name"),
        "order_date": order_details.get("order_date"),
        "order_type": order_details.get("order_type"),
        "qty": order_details.get("qty"),
        "price": order_details.get("price"),
        "total_amount": order_details.get("total_amount"),
        "total_investment": order_details.get("price") * order_details.get("qty"),
        "bank_account_name": bank_details.get("account_name"),
        "bank_account_number": bank_details.get("account_number"),
        "bank_name": bank_details.get("bank_name"),
        "bank_branch": bank_details.get("branch"),
        "bank_ifsc": bank_details.get("ifsc"),
        "whatsapp_link": whatsapp_link,
        "website_url": website_url,
        "logo_url": logo_url,
        "unsubscribe_link": unsubscribe_link,
    }

    # Render the email template
    email_body = render_to_string("finvest_finance/accounts/templates/order_email.html", context)

    # Send the email
    send_mail(
        subject="Order Confirmation: Purchase of Shares",
        message="",
        html_message=email_body,
        from_email="noreply@faanfinvest.com",
        recipient_list=[email],
        fail_silently=False,
    )


def send_confirmation_email(user_name, email, confirmation_details, whatsapp_link, website_url, logo_url, unsubscribe_link):
    # Context for the confirmation email template
    context = {
        "user_name": user_name,
        "confirmation_message": confirmation_details.get("message"),
        "share_name": confirmation_details.get("share_name"),
        "confirmation_date": confirmation_details.get("confirmation_date"),
        "qty": confirmation_details.get("qty"),
        "price": confirmation_details.get("price"),
        "total_amount": confirmation_details.get("total_amount"),
        "whatsapp_link": whatsapp_link,
        "website_url": website_url,
        "logo_url": logo_url,
        "unsubscribe_link": unsubscribe_link,
    }

    # Render the email template
    email_body = render_to_string("finvest_finance/accounts/templates/confirmation.html", context)

    # Send the email
    send_mail(
        subject="Confirmation: Share Purchase Completed",
        message="",
        html_message=email_body,
        from_email="noreply@faanfinvest.com",
        recipient_list=[email],
        fail_silently=False,
    )
