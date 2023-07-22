from django.db import models
from tenants.models import Tenant
from leases.models import Lease
from property.models import Units

# Create your models here.
class RentPayment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE,related_name='payments')
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE,related_name='payments')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description=models.CharField(max_length=100, choices=(("rent_installment","Rent Installment"),("rent_in_full","Rent in full")))
    date_paid = models.DateField()
    outstanding_balance = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.tenant} - {self.amount}"

class RentDeposits(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE,related_name='deposits')
    property_unit = models.ForeignKey(Units, on_delete=models.CASCADE,related_name='deposits')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description=models.CharField(max_length=100, choices=(("commitment_fee","Commitment Fee"),("deposit_in_full","Deposit in full")))
    date_paid = models.DateField()
    outstanding_balance = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.tenant} - {self.amount}"

