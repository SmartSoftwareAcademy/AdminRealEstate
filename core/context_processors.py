from .models import *
from django.utils import timezone
from django.conf import settings
from tenants.models import Tenant
from landlords.models import PropertyOwner,Agent
from notices.models import Notice,Enquiries
from property.models import Property,Units
from leases.models import Lease
from django.shortcuts import redirect

def site_defaults(request):
    if not request.user.is_authenticated:
        return {}
    setup=Setup.objects.first()
    if setup !=None:
       logo=setup.logo
    else:
        logo=settings.MEDIA_URL+'logo/default.png'

    vals = SiteConfig.objects.all()
    contexts = {
        "site_logo":logo,
        "tenant_count":Tenant.objects.count(),
        "owner_count":PropertyOwner.objects.count(),
        "agent_count":Agent.objects.count(),
        "notice_count":Notice.objects.filter(read=False,user_to_notify=request.user).count() if request.user.is_authenticated else 0,
        "enquiry_count":Enquiries.objects.filter(read=False).count(),
        "properties_count":Property.objects.count(),
        "active_lease_count":Lease.objects.filter(is_active=True).count(),
        "dormant_lease_count":Lease.objects.filter(is_active=False).count(),
    }
    for val in vals:
        contexts[val.key] = val.value

    return contexts
