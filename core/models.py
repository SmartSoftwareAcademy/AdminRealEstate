from django.db import models
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField
from property.models import Property

User=get_user_model()

# Create your models here.
class SiteConfig(models.Model):
    """Site Configurations"""
    key = models.SlugField()
    value = models.CharField(max_length=200)
    config_id=models.IntegerField(default=1)
    picked=models.BooleanField(default=False)

    def __str__(self):
        return self.key

class Setup(models.Model):
    logo=models.ImageField(upload_to='logo/',default='logo/default.png')
    support_reply_email_name = models.CharField(
        max_length=255, default='ICT Helpdesk', blank=True, null=True)
    support_reply_email = models.EmailField(
        max_length=255, default='titusowuor30@gmail.com', blank=True, null=True)
    email_password = models.CharField(
        max_length=255, default='xdofqrtncuimlewm', blank=True, null=True)
    email_port = models.IntegerField(default=587, blank=True, null=True)
    email_backed = models.CharField(
        max_length=100, default='smtp', blank=True, null=True)
    email_host = models.CharField(
        max_length=255, default='smtp.gmail.com', blank=True, null=True)
    fail_silently = models.BooleanField(default=True, blank=True, null=True)
    use_tls = models.BooleanField(default=True, blank=True, null=True)
    code_place_holders = models.TextField(
        max_length=25000, blank=True, null=True)


    def __str__(self):
        return self.logo.url if self.logo else 'logo/default.png'

    class Meta:
        verbose_name_plural='Site Setup'


class Testimonial(models.Model):
    property=models.ForeignKey(Property,on_delete=models.CASCADE,blank=True,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    designation=models.CharField(max_length=100,default="Engineer, EAT Steel EAC",help_text="Enter profession and position separated by comma")
    rating=models.CharField(max_length=1,choices=(("1",1),("2",2),("3",3),("4",4),("5",5)),default="5")
    content = HTMLField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural='testimonials'
        db_table='testimonials'
        managed=True


class About(models.Model):
    property=models.ForeignKey(Property,on_delete=models.CASCADE)
    content = HTMLField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.property.property_name

    class Meta:
        verbose_name_plural='about content'
        db_table='about_content'
        managed=True

class Services(models.Model):
    property=models.ForeignKey(Property,on_delete=models.CASCADE)
    service_name=models.CharField(max_length=100)
    service_img_or_icon=models.ImageField(upload_to='services',blank=True,null=True)
    content = HTMLField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.property.property_name

    class Meta:
        verbose_name_plural='Services'
        db_table='services'
        managed=True

