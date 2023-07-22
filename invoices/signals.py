# # signals.py

# from datetime import timedelta
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.utils import timezone
# from .models import Lease, Invoice
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# #from apscheduler.schedulers.background import BackgroundScheduler

# scheduler = BackgroundScheduler()

# def send_invoice_email(lease_id):
#     lease = Lease.objects.get(pk=lease_id)
#     tenant = lease.tenant
#     invoice = Invoice.objects.create(
#         lease=lease,
#         invoice_type='rent',
#         amount=lease.monthly_rent,
#         description='Rent Invoice',
#         due_date=lease.start_date,
#         is_paid=False
#     )
#     email_subject = f'Invoice for Lease: {lease}'
#     email_body = render_to_string('invoices/invoice_email.html', {'invoice': invoice})
#     send_mail(email_subject, '', '', [tenant.user.email], html_message=email_body)

# @receiver(pre_save, sender=Lease)
# def schedule_invoice_creation(sender, instance, **kwargs):
#     if instance.is_active and not instance.end_date:
#         two_days_before = instance.start_date - timedelta(days=2)
#         if timezone.now().date() >= two_days_before:
#             scheduler.add_job(send_invoice_email, 'date', args=[instance.id], run_date=timezone.now())
#             scheduler.start()
