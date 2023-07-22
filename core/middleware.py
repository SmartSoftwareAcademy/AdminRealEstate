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
        response = self.get_response(request)

        return response
