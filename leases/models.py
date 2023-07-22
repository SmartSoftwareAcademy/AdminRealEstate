from django.db import models
from tenants.models import Tenant
from property.models import Property,Units
from django.db import models
from datetime import date
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
User=get_user_model()

class Lease(models.Model):
    property_unit = models.ForeignKey(Units, on_delete=models.CASCADE, related_name='leases')
    leased_by=models.ForeignKey(User,on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='leases')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now,blank=True,null=True)
    monthly_rent = models.DecimalField(max_digits=8, decimal_places=2,default=2000)
    security_deposit = models.DecimalField(max_digits=8, decimal_places=2,default=2000)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.property_unit} - {self.tenant}"

    def is_expired(self):
        return self.end_date < date.today()

    class Meta:
        verbose_name_plural = "Leases"
        db_table = "leases"

    def get_absolute_url(self):
        return reverse("lease-detail", kwargs={"pk": self.pk})

class LeaseTerm(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='terms')
    late_payment_fine=models.DecimalField(max_digits=8, decimal_places=2,default=0)
    uilities_description=models.CharField(max_length=500,default='Electricity,Water,Gabbage management,swimming pool,gym')
    utilities_amount=models.DecimalField(max_digits=8, decimal_places=2,default=0)
    term_number = models.PositiveIntegerField(default=1001)
    term_description=models.TextField(max_length=500,default='Description here')
    accepted=models.BooleanField(default=False)

    def __str__(self):
        return f"Term {self.term_number} - {self.lease}"

    class Meta:
        verbose_name_plural = "Lease Terms"
        db_table = "lease_terms"

    def get_absolute_url(self):
        return reverse("lease-detail", kwargs={"pk": self.pk})