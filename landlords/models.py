from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import RegexValidator

User=get_user_model()
mobile_num_regex = RegexValidator(
        regex=r"^(?:\+254|0)[17]\d{8}$", message="Entered mobile number isn't in a right format!"
    )

# Create your models here.
class PropertyOwner(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='owners')
    mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )
    national_id=models.CharField(max_length=10,blank=True,null=True)
    ID_Snapshot=models.ImageField(upload_to='owners/documents/',blank=True,null=True)

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("property-owner-detail", kwargs={"pk": self.pk})


class Agent(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='agents')
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE, related_name='agents')
    mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )
    national_id=models.CharField(max_length=10,blank=True,null=True)
    ID_Snapshot=models.ImageField(upload_to='owners/documents/',blank=True,null=True)

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("agent-detail", kwargs={"pk": self.pk})