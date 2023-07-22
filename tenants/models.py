from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from landlords.models import Agent,PropertyOwner

User=get_user_model()
mobile_num_regex = RegexValidator(
        regex=r"^(?:\+254|0)[17]\d{8}$", message="Entered mobile number isn't in a right format!"
    )

class Tenant(models.Model):
    STATUS = [("active", "Active"), ("inactive", "Inactive")]
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='tenants')
    created_by=models.ForeignKey(User, on_delete=models.CASCADE)
    current_status = models.CharField(
        max_length=10, choices=STATUS, default="active")
    date_of_birth=models.DateField(max_length=200,default=timezone.now())
    National_ID = models.CharField(max_length=10,default='899338')
    date_of_registration = models.DateField(default=timezone.now)
    mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )
    others = models.TextField(blank=True,null=True,default='N/A')

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("tenant-detail", kwargs={"pk": self.pk})

class Tenant_Kin(models.Model):
    tenant=models.ForeignKey(Tenant,on_delete=models.CASCADE,related_name='kins')
    name=models.CharField(max_length=200)
    phone = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
     )
    relation=models.CharField(max_length=100)
    emergency_name=models.CharField(max_length=100)
    emergency_phone_number = models.CharField(validators=[mobile_num_regex], max_length=13, blank=True)
    emergency_email=models.EmailField(max_length=100)
    emergency_adress=models.TextField(max_length=500)
    emergency_physical_adress=models.TextField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
       verbose_name_plural="Kins"
       managed=True

    def get_absolute_url(self):
        return reverse("kin-detail", kwargs={"pk": self.pk})


class Tenant_Employment_Details(models.Model):
    tenant=models.ForeignKey(Tenant,on_delete=models.CASCADE,related_name='employments')
    employment_status = models.CharField(max_length=50, choices=(("employed","employed"),("unemployed","unemployed"),("selfemployed","selfemployed")))
    emplyment_title=models.CharField(max_length=100)
    employment_postion=models.CharField(max_length=100)
    employer_contact = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )
    employer_email=models.EmailField(max_length=100)
    employer_address=models.TextField(max_length=500)

    def __str__(self):
        return self.employment_status

    class Meta:
       verbose_name_plural="Employment Details"
       managed=True

class Tenant_Business_Details(models.Model):
    tenant=models.ForeignKey(Tenant,on_delete=models.CASCADE,related_name='businesses')
    business_name=models.CharField(max_length=100)
    license_number=models.CharField(max_length=100)
    tax_id=models.CharField(max_length=100)
    business_email=models.EmailField(max_length=100)
    business_address=models.TextField(max_length=500)
    business_description=models.TextField(max_length=500)

    def __str__(self):
        return self.business_name
    class Meta:
       verbose_name_plural="Business Details"
       managed=True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            PropertyOwner.objects.create(user=instance)
        if instance.user_type == 2:
            Agent.objects.create(user=instance)
        if instance.user_type == 3:
            Tenant.objects.create(user=instance)