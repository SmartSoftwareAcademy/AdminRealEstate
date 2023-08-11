from django.db import models
from invoices.models import Invoice
from tinymce.models import HTMLField

# Create your models here.
class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,related_name='invoices',blank=True,null=True)
    payment_method=models.CharField(max_length=100,default='cash',choices=(("mobile","Mobile Money"),("bank","Bank API"),("cash","Cash")))
    transaction_code=models.CharField(max_length=16,default='X4&HJJK')
    amount = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    description=HTMLField(max_length=500, default="Rent Installment")
    date_paid = models.DateField()
    outstanding_balance = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.invoice.invoice_id} - {self.amount}"

# class RentDeposits(models.Model):
#     tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE,related_name='deposits')
#     property_unit = models.ForeignKey(Units, on_delete=models.CASCADE,related_name='deposits')
#     amount = models.DecimalField(max_digits=8, decimal_places=2)
#     description=models.CharField(max_length=100, choices=(("commitment_fee","Commitment Fee"),("deposit_in_full","Deposit in full")))
#     date_paid = models.DateField()
#     outstanding_balance = models.DecimalField(max_digits=8, decimal_places=2)

#     def __str__(self):
#         return f"{self.tenant} - {self.amount}"

