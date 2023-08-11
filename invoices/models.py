from django.db import models
from leases.models import Lease
from datetime import datetime,timedelta

# Create your models here.
class Invoice(models.Model):
    INVOICE_TYPES = [
        ('rent', 'Rent'),
        ('utility', 'Utility'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other'),
    ]
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='invoices')
    invoice_id= models.CharField(max_length=100,default='202222300001')
    invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPES)
    amount = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    balance = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    description = models.TextField(max_length=1500)
    status = models.CharField(max_length=50,default='Pending',choices=(("Paid","Paid"),("Pending","Pending"),("Partial","Partial")))
    due_date = models.DateField(default=datetime.now()+timedelta(days=5))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.invoice_type} Invoice for Lease: {self.lease}"

    class Meta:
        ordering = ['-created_at']
