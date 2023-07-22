from django.contrib import admin
from .models import *


@admin.register(SiteConfig)
class PropertyOwnerAdmin(admin.ModelAdmin):
    list_display = ('key', 'value',)
    list_filter = ('key','value',)
    search_fields = ('key', 'value',)

@admin.register(Setup)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('support_reply_email_name','support_reply_email','email_password','email_port','email_backed','email_host','fail_silently','use_tls')
    list_filter = ('support_reply_email_name','support_reply_email','email_password','email_port','email_backed','email_host','fail_silently','use_tls')
    search_fields =('support_reply_email_name','support_reply_email','email_password','email_port','email_backed','email_host','fail_silently','use_tls')

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