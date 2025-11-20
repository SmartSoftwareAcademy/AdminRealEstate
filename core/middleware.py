from .models import *
from account.models import *
from django.utils import timezone
from django.contrib.auth import get_user_model

User=get_user_model()

class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        user=User.objects.filter(email='admin@admin.com').first()
        if user == None:
           User.objects.create(username='admin',email='admin@admin.com',password='@Admin123')
        else:
            user.username='admin'
            user.first_name='admin'
            user.last_name='admin'
            user.save()
        configdict={"site_title":"Real Estate Admin","site_slogan":"Create . Innovate . Excel","site_addres":"Excel Building, Kisumu, 1235 St.","site_email":"info@ferbrook.co.ke|www.ferbrookapartments.co.ke","tel":"+2547 000 000 001"}
        configs=SiteConfig.objects.count()
        if configs ==0:
            for k,v in configdict.items():
              sc,created=SiteConfig.objects.get_or_create(key=k,value=v)
        # Seed email & Mpesa config if missing so it can be edited via admin
        setup, created = Setup.objects.get_or_create(
            pk=1,
            defaults={
                'support_reply_email_name': 'Bengo Mall KE',
                'support_reply_email': 'bengomallke@gmail.com',
                'email_password': '',  # User should set this via admin panel
                'email_host': 'smtp.gmail.com',
                'email_port': 587,
                'email_backed': 'smtp',
                'use_tls': True,
                'fail_silently': True,
                # Mpesa Sandbox defaults - can be updated via admin panel
                # Default sandbox shortcode: 174379 (standard Safaricom test shortcode)
                # Default sandbox passkey: Provided by Safaricom for testing
                # Users can get their own credentials from: https://developer.safaricom.co.ke
                'mpesa_environment': 'sandbox',
                'mpesa_consumer_key': 'cHnkwYIgBbrxlgBoneczmIJFXVm0oHky',  # Default sandbox test key
                'mpesa_consumer_secret': '2nHEyWSD4VjpNh2g',  # Default sandbox test secret
                'mpesa_business_short_code': '174379',  # Default sandbox test shortcode
                'mpesa_passkey': 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919',  # Default sandbox passkey
                'mpesa_callback_url': 'https://example.com/payments/mpesa/callback/',  # Update with your ngrok/public URL via admin
            }
        )
        
        # Auto-fill empty Mpesa fields with defaults (for both new and existing instances)
        from payments.mpesa_credentials import MpesaConfig
        needs_save = False
        
        # Ensure environment is set
        if not setup.mpesa_environment:
            setup.mpesa_environment = 'sandbox'
            needs_save = True
        
        # Auto-fill sandbox defaults if environment is sandbox
        if setup.mpesa_environment == 'sandbox':
            # Auto-fill consumer key if empty
            if not setup.mpesa_consumer_key:
                setup.mpesa_consumer_key = MpesaConfig.DEFAULT_CONSUMER_KEY
                needs_save = True
            
            # Auto-fill consumer secret if empty
            if not setup.mpesa_consumer_secret:
                setup.mpesa_consumer_secret = MpesaConfig.DEFAULT_CONSUMER_SECRET
                needs_save = True
            
            # Auto-fill business shortcode if empty
            if not setup.mpesa_business_short_code:
                setup.mpesa_business_short_code = MpesaConfig.DEFAULT_BUSINESS_SHORT_CODE
                needs_save = True
            
            # Auto-fill passkey if empty (especially if consumer key/secret are set)
            if not setup.mpesa_passkey:
                setup.mpesa_passkey = MpesaConfig.DEFAULT_PASSKEY
                needs_save = True
            
            # Auto-fill callback URL if empty (use default)
            if not setup.mpesa_callback_url:
                setup.mpesa_callback_url = MpesaConfig.DEFAULT_CALLBACK_URL
                needs_save = True
        
        # Save if any defaults were filled
        if needs_save:
            setup.save()
        response = self.get_response(request)

        return response
