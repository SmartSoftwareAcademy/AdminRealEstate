from django.contrib import admin
from .models import *


@admin.register(SiteConfig)
class PropertyOwnerAdmin(admin.ModelAdmin):
    list_display = ('key', 'value',)
    list_filter = ('key','value',)
    search_fields = ('key', 'value',)

@admin.register(Setup)
class SetupAdmin(admin.ModelAdmin):
    list_display = (
        'support_reply_email_name',
        'support_reply_email',
        'email_host',
        'email_port',
        'use_tls',
        'mpesa_environment',
        'mpesa_business_short_code',
    )
    list_filter = (
        'support_reply_email',
        'email_host',
        'use_tls',
        'mpesa_environment',
        'mpesa_business_short_code',
    )
    search_fields = (
        'support_reply_email_name',
        'support_reply_email',
        'email_host',
        'mpesa_business_short_code',
    )
    
    def has_add_permission(self, request):
        # Only allow one Setup instance
        return Setup.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the Setup instance
        return False
    
    def save_model(self, request, obj, form, change):
        """
        Auto-fill sandbox defaults when consumer key/secret are configured.
        - If sandbox environment and shortcode is empty, use default 174379
        - If sandbox environment and passkey is empty but consumer key/secret are set, use default passkey
        """
        # Default sandbox credentials
        DEFAULT_SANDBOX_SHORTCODE = '174379'
        DEFAULT_SANDBOX_PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        
        # Ensure environment is set
        if not obj.mpesa_environment:
            obj.mpesa_environment = 'sandbox'
        
        # Auto-fill sandbox defaults
        if obj.mpesa_environment == 'sandbox':
            # Auto-fill shortcode if empty
            if not obj.mpesa_business_short_code:
                obj.mpesa_business_short_code = DEFAULT_SANDBOX_SHORTCODE
            
            # Auto-fill passkey if consumer key/secret are configured but passkey is empty
            if obj.mpesa_consumer_key and obj.mpesa_consumer_secret and not obj.mpesa_passkey:
                obj.mpesa_passkey = DEFAULT_SANDBOX_PASSKEY
        
        super().save_model(request, obj, form, change)
    fieldsets = (
        ('Site Logo', {
            'fields': ('logo',)
        }),
        ('Email Configuration', {
            'fields': (
                'support_reply_email_name',
                'support_reply_email',
                'email_password',
                'email_host',
                'email_port',
                'email_backed',
                'use_tls',
                'fail_silently',
            ),
            'description': 'Configure SMTP settings for sending emails. Default uses Gmail (smtp.gmail.com:587). For Gmail, use an App Password instead of your regular password.'
        }),
        ('Mpesa Daraja API Configuration', {
            'fields': (
                'mpesa_environment',
                'mpesa_consumer_key',
                'mpesa_consumer_secret',
                'mpesa_business_short_code',
                'mpesa_passkey',
                'mpesa_callback_url',
            ),
            'description': '''Configure Mpesa Daraja API credentials.
            
SANDBOX (Testing):
- Register at https://developer.safaricom.co.ke and create an app to get Consumer Key and Consumer Secret
- Default Sandbox Shortcode: 174379 (auto-filled if empty)
- Default Sandbox Passkey: Auto-filled when Consumer Key/Secret are configured
- You can get your own passkey from: Developer Portal -> My Apps -> Your App -> Test Credentials

PRODUCTION (Live):
- Use credentials from your Safaricom Business account
- All fields must be configured manually

IMPORTANT: Update the callback URL with your public HTTPS URL (use ngrok for local testing).'''
        }),
        ('Advanced', {
            'fields': ('code_place_holders',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'published', 'created_at')
    list_filter = ('published', 'created_at')
    search_fields = ('user', 'content')

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('property','service_name','content','published', 'created_at')
    list_filter =  ('property','service_name','content','published', 'created_at')
    search_fields =  ('property','service_name','content','published', 'created_at')

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('property', 'published', 'created_at')
    list_filter = ('published', 'created_at')
    search_fields = ('property', 'content')