from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.urls import reverse

User=get_user_model()
mobile_num_regex = RegexValidator(
        regex=r"^(?:\+254|0)[17]\d{8}$", message="Entered mobile number isn't in a right format!"
    )
# Create your models here.
class Staff(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name='staff')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_ower')
    mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )
    national_id=models.CharField(max_length=10,blank=True,null=True)
    ID_Snapshot=models.ImageField(upload_to='staff/documents/',blank=True,null=True)
    position = models.CharField(max_length=100)
    date_of_joining = models.DateField()

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = "Staff"
        db_table = "staff"

    def get_absolute_url(self):
        return reverse("staff-detail", kwargs={"pk": self.pk})


class StaffSalary(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='salary_details')
    earnings = models.ManyToManyField("Earning")
    deductions = models.ManyToManyField("Deduction")
    net_salary = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def __str__(self):
        return f"{self.net_salary}"

    class Meta:
        verbose_name_plural = "Staff Salary Details"
        db_table = "staff_salary"

    def get_absolute_url(self):
        return reverse("salary-detail", kwargs={"pk": self.pk})

    def calculate_net_pay(self):
        total_earnings = sum(self.earnings.values_list('amount', flat=True))
        total_deductions = sum(self.deductions.values_list('amount', flat=True))
        print(total_earnings,total_deductions)
        self.net_salary = total_earnings - total_deductions
        self.save()


class Earning(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='earnings')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}({self.amount}) {self.staff}"

class Deduction(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='deductions')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}({self.amount}) {self.staff}"


