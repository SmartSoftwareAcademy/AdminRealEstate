
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
    notice_type=models.CharField(max_length=100,choices=(("vacate","Vacate Notice"),("mainatainance","Maintainace"),("welcome","Welcome Notice")))
    notify_specific_user= models.ForeignKey(User, on_delete=models.CASCADE,related_name='notices',blank=True,null=True,help_text='Leave Blank if not applicable')
    notify_group_of_users= models.CharField(max_length=50,choices=(("1","Owner"),("2","Agent"),("3","Staff"),("4","Tenant")),blank=True,null=True,help_text='Leave Blank if not applicable')
    notice_date = models.DateField()
    description = HTMLField(default="<h1>WELCOME NEW TENANT</h1><h4>Dear Mr./Mrs./Miss</h4>\
                                     <p>It is our pleasure to welcome you to your new home. We hope that you will be very happy here and will try our best to make sure that you are always satisfied.\
                                     <br/>Thankyou for selecting Fernbrook Apartments and we sincerely hope that you find your new home comfortable and enjoyable.\
                                     <br/>If we can be of any assistance to you, please let us know.\
                                     <br/>I can be reached at + 1(952) 210 0808 at any time. Rosemary can be reached at +1(763)458 6243.\
                                     <br/><br/><strong>Yours sincerely,\
                                     <br/>Wycliffe George/ Director</strong></p>")
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
