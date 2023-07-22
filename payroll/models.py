from django.db import models
from django.urls import reverse
from staff.models import Staff,Earning,Deduction

# Create your models here.
class StaffSalaryPayment(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='payments')
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    date_of_pyament=models.DateTimeField(auto_now_add=True)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def __str__(self):
        return f"{self.staff.user.email} - {self.month}/{self.year}"


    class Meta:
        verbose_name_plural = "Payroll"
        db_table = "staff_payments"

    def get_absolute_url(self):
        return reverse("staff-payment-detail", kwargs={"pk": self.pk})