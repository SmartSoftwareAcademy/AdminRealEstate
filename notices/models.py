
from django.db import models
from django.utils import timezone
from django.urls import reverse
from property.models import *
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import RegexValidator
from tinymce.models import HTMLField

User=get_user_model()

mobile_num_regex = RegexValidator(
        regex=r"^(?:\+254|0)[17]\d{8}$", message="Entered mobile number isn't in a right format!"
    )
# Create your models here.
class Notice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notice_type=models.CharField(max_length=100,choices=(("vacate","Vacate Notice"),("mainatainance","Maintainace")))
    user_to_notify = models.ForeignKey(User, on_delete=models.CASCADE,related_name='notices')
    notice_date = models.DateField()
    description = HTMLField()
    reason=models.CharField(max_length=255,default='Reason here',blank=True,null=True)
    read=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.notice_type} - {self.notice_date}"

    def get_absolute_url(self):
        return reverse("notice-detail", kwargs={"pk": self.pk})

class NoticeFeedback(models.Model):
    notice=models.ForeignKey(Notice,on_delete=models.CASCADE,related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notice_date = models.DateField(auto_now_add=True)
    reply = HTMLField()
    read=models.BooleanField(default=False)

    def __str__(self):
        return self.notice.description

    def get_absolute_url(self):
        return reverse("reply-detail", kwargs={"pk": self.pk})

class Enquiries(models.Model):
    fullname = models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )
    date = models.DateField(auto_now_add=True)
    message=HTMLField()
    read=models.BooleanField(default=False)


    def __str__(self):
        return f"{self.fullname} - {self.message}"

    def get_absolute_url(self):
        return reverse("notice-detail", kwargs={"pk": self.pk})
