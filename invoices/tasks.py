# tasks.py

from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Invoice
from leases.models import Lease

@shared_task
def generate_invoices():
    # Get leases that have expired
    expired_leases = Lease.objects.filter(end_date__gte=timezone.now(), is_active=True)

    for lease in expired_leases:
        # Check if an invoice already exists for this lease
        existing_invoice = Invoice.objects.filter(lease=lease).exists()
        if not existing_invoice:
            # Create a new invoice
            Invoice.objects.create(
                lease=lease,
                invoice_type='rent',  # You can change this based on your requirement
                amount=lease.monthly_rent,
                balance=lease.monthly_rent,
                description=f'Rent invoice for lease {lease.id}',
                status='Pending',
                due_date=timezone.now() + timedelta(days=5)
            )
