# scheduler.py

from datetime import timedelta
from django_apscheduler.jobstores import register_events
from django_apscheduler.models import DjangoJob, DjangoJobExecution
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Lease, Invoice
from django.core.mail import send_mail
from django.template.loader import render_to_string

def create_invoice_on_lease_expiration():
    leases = Lease.objects.filter(is_active=True, end_date__isnull=True)
    for lease in leases:
        two_days_before = lease.start_date - timedelta(days=2)
        if lease.start_date.date() >= two_days_before:
            tenant = lease.tenant
            invoice = Invoice.objects.create(
                lease=lease,
                invoice_type='rent',
                amount=lease.monthly_rent,
                description='Rent Invoice',
                due_date=lease.start_date,
                is_paid=False
            )
            email_subject = f'Invoice for Lease: {lease}'
            email_body = render_to_string('invoice_email.html', {'invoice': invoice})
            send_mail(email_subject, '', '', [tenant.user.email], html_message=email_body)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(create_invoice_on_lease_expiration, 'interval', days=1)
    scheduler.start()
    register_events(scheduler)
