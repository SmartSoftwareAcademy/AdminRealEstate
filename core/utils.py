
import re
from django.core.mail.backends.smtp import EmailBackend
# from django.core.mail import EmailMessage
from .models import Setup
from django.db.models import Sum,F
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from invoices.models import Invoice
from datetime import datetime
from payments.models import Payment

class MailSender:
    def __init__(self, request, subject, body, to, attachments=[]):
        self.subject = subject
        self.body = body
        self.to = to,
        self.attachments = attachments
        self.request = request

    def send_email(self):
        try:
            config = Setup.objects.first()
            backend = EmailBackend(
                host=config.email_host,
                port=config.email_port,
                username=config.support_reply_email,
                password=config.email_password,
                use_tls=config.use_tls,
                fail_silently=config.fail_silently
            )

            # Process the email body as HTML
            message_html = self.body

            # Replace &nbsp; with space
            message_text = re.sub(r'(?<!&nbsp;)&nbsp;', ' ', strip_tags(self.body))

            if self.attachments:
                email = EmailMultiAlternatives(
                    subject=self.subject,
                    body=message_text,
                    from_email=config.support_reply_email,
                    to=self.to,
                    connection=backend
                )
                email.attach_alternative(message_html, "text/html")

                for attch in self.attachments:
                    email.attach(attch.name, attch.read(), attch.content_type)

                email.send()
                messages.success(self.request, 'Email sent successfully!')
            else:
                email = EmailMultiAlternatives(
                    subject=self.subject,
                    body=message_text,
                    from_email=config.support_reply_email,
                    to=self.to,
                    connection=backend
                )
                email.attach_alternative(message_html, "text/html")
                email.send()
                messages.success(self.request, 'Email sent successfully!')
        except Exception as e:
            print(e)
            messages.info(self.request, "Email send error: {}".format(e))

def tenant_rent_analytics(tenant_user):
    # Calculate total amount of rent paid by the tenant
    total_rent_paid = Invoice.objects.filter(
        lease__tenant__user=tenant_user,
        invoice_type='rent',
        status='Paid'
    ).aggregate(total_rent_paid=Sum('amount'))['total_rent_paid'] or 0

    # Calculate total rent owed by the tenant
    total_rent_owed = Invoice.objects.filter(
        lease__tenant__user=tenant_user,
        invoice_type='rent',
        status='Pending'
    ).aggregate(total_rent_owed=Sum('balance'))['total_rent_owed'] or 0

    # Calculate total amount of partial payments
    total_partial_payments = Invoice.objects.filter(
        lease__tenant__user=tenant_user,
        invoice_type='rent',
        status='Partial'
    ).aggregate(total_partial_payments=Sum('amount')-Sum('balance'))['total_partial_payments'] or 0

    # Calculate total amount of partially owed payments
    total_owed_partial_payments = Invoice.objects.filter(
        lease__tenant__user=tenant_user,
        invoice_type='rent',
        status='Partial'
    ).aggregate(total_owed_partial_payments=Sum('balance'))['total_owed_partial_payments'] or 0

    # Calculate actual rent paid and actual rent owed
    actual_rent_paid = total_rent_paid + total_partial_payments
    actual_rent_owed = total_rent_owed + total_owed_partial_payments

    return actual_rent_paid, actual_rent_owed

#Yearly rent analytics
def get_rent_payment_analytics(year):
    analytics = []
    for month in range(1, 13):
        month_start = datetime(year, month, 1)
        month_end = month_start.replace(day=30) if month != 2 else month_start.replace(day=28)

        total_payments = Payment.objects.filter(
            date_paid__range=(month_start, month_end),
            invoice__invoice_type='rent',
            invoice__status='Paid'
        ).values("invoice__amount").aggregate(total=Sum('invoice__amount'))['total'] or 0

        total_partial_payments = Payment.objects.filter(
            date_paid__range=(month_start, month_end),
            invoice__invoice_type='rent',
            invoice__status='Partial'
        ).values("invoice__balance","invoice__amount","invoice__lease__tenant").distinct().aggregate(total=Sum('invoice__amount')-Sum("invoice__balance"))['total'] or 0

        analytics.append({'month': month, 'total_payments': total_payments+total_partial_payments})

    return analytics

