from django.db import models
from leases.models import Lease
# Create your models here.
class Invoice(models.Model):
    INVOICE_TYPES = [
        ('rent', 'Rent'),
        ('utility', 'Utility'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other'),
    ]
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='invoices')
    invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPES)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(max_length=1500)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.invoice_type} Invoice for Lease: {self.lease}"

    class Meta:
        ordering = ['-created_at']
