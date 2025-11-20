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
        max_length=255, default='ICT Helpdesk', blank=True, null=True,
        help_text="Display name for email sender (e.g., 'Real Estate Admin')")
    support_reply_email = models.EmailField(
        max_length=255, default='bengomallke@gmail.com', blank=True, null=True,
        help_text="Email address used to send notifications. For Gmail, use an App Password (not your regular password).")
    email_password = models.CharField(
        max_length=255, default='xdofqrtncuimlewm', blank=True, null=True,
        help_text="Email password or App Password. For Gmail: Generate App Password from Google Account > Security > 2-Step Verification > App Passwords")
    email_port = models.IntegerField(default=587, blank=True, null=True,
        help_text="SMTP port: 587 (TLS) or 465 (SSL). Default: 587 for Gmail.")
    email_backed = models.CharField(
        max_length=100, default='smtp', blank=True, null=True,
        help_text="Email backend type. Usually 'smtp' for SMTP servers.")
    email_host = models.CharField(
        max_length=255, default='smtp.gmail.com', blank=True, null=True,
        help_text="SMTP server hostname. Gmail: smtp.gmail.com | Outlook: smtp-mail.outlook.com | Custom: your-domain.com")
    fail_silently = models.BooleanField(default=True, blank=True, null=True,
        help_text="If True, email errors won't raise exceptions (useful for production).")
    use_tls = models.BooleanField(default=True, blank=True, null=True,
        help_text="Enable TLS encryption for SMTP. Required for Gmail (port 587).")
    code_place_holders = models.TextField(
        max_length=25000, blank=True, null=True)
    # Mpesa configuration (sandbox by default)
    mpesa_consumer_key = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Mpesa Daraja API Consumer Key. Sandbox: Get from https://developer.safaricom.co.ke | Production: From your Safaricom Business account.")
    mpesa_consumer_secret = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Mpesa Daraja API Consumer Secret. Sandbox: Get from https://developer.safaricom.co.ke | Production: From your Safaricom Business account.")
    mpesa_business_short_code = models.CharField(
        max_length=20, blank=True, null=True,
        help_text="Mpesa Business Short Code (Paybill/Till). Sandbox: Default is 174379 (auto-filled if empty) | Production: Your registered Paybill/Till number.")
    mpesa_passkey = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Mpesa Daraja API Passkey (Lipa na Mpesa Online Passkey). Sandbox: Default passkey is auto-filled if Consumer Key/Secret are configured. Get your own from https://developer.safaricom.co.ke -> My Apps -> Test Credentials | Production: From your Safaricom Business account.")
    mpesa_callback_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        default='https://example.com/payments/mpesa/callback/',
        help_text="Public URL where Mpesa will send payment callbacks. Must be HTTPS and publicly accessible. Use ngrok for local testing: https://your-ngrok-url.ngrok.io/payments/mpesa/callback/"
    )
    mpesa_environment = models.CharField(
        max_length=20,
        choices=[('sandbox', 'Sandbox (Testing)'), ('production', 'Production (Live)')],
        default='sandbox',
        blank=True,
        null=True,
        help_text="Select 'Sandbox' for testing with test credentials, or 'Production' for live transactions."
    )


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

