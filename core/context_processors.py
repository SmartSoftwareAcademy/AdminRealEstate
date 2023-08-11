from .models import *
from django.utils import timezone
from django.conf import settings
from tenants.models import Tenant
from landlords.models import PropertyOwner,Agent
from notices.models import Notice,Enquiries
from property.models import Property,Units
from leases.models import Lease
from invoices.models import Invoice
from django.shortcuts import redirect
from django.db.models import Q
from staff.models import Staff
from payroll.models import StaffSalaryPayment

def site_defaults(request):
    if not request.user.is_authenticated:
        return {}
    setup=Setup.objects.first()
    if setup !=None:
       logo=setup.logo
    else:
        logo=settings.MEDIA_URL+'logo/default.png'

    vals = SiteConfig.objects.all()
    #load welcome notice
    note=Notice.objects.filter(Q(notice_type="welcome") & Q(read=False) & (Q(notify_specific_user=request.user) | Q(notify_group_of_users=request.user.user_type))).first()
    if note:
       note.description=note.description.replace("Dear Mr./Mrs./Miss",f"Dear Mr./Mrs./Miss <b>{request.user},</b>")
    contexts = {
        "site_logo":logo,
        "tenant_count":Tenant.objects.count() if len(Tenant.objects.all()) > 0 else 0,
        "owner_count":PropertyOwner.objects.count() if len(PropertyOwner.objects.all()) > 0 else 0,
        "agent_count":Agent.objects.count() if len(Agent.objects.all()) > 0 else 0,
        "staff_count":Staff.objects.count() if len(Staff.objects.all()) > 0 else 0,
        "payslip_count":StaffSalaryPayment.objects.count() if len(StaffSalaryPayment.objects.all()) > 0 else 0,
        "notice_count":Notice.objects.filter(Q(read=False) & (Q(notify_specific_user=request.user) | Q(notify_group_of_users=request.user.user_type))).count() if len(Notice.objects.all()) > 0 else 0,
        "enquiry_count":Enquiries.objects.filter(Q(read=False) & Q(email=request.user.email)).count() if len(Enquiries.objects.all()) > 0 else 0,
        "properties_count":Property.objects.count() if len(Property.objects.all()) > 0 else 0,
        "active_lease_count":Lease.objects.filter(is_active=True).count() if len(Lease.objects.all()) > 0 else 0,
        "dormant_lease_count":Lease.objects.filter(is_active=False).count() if len(Lease.objects.all()) > 0 else 0,
        "welcome_note":note if note else [],
        "notices":Notice.objects.filter(Q(read=False) & (Q(notify_specific_user=request.user) | Q(notify_group_of_users=request.user.user_type))).exclude(notice_type="welcome") if len(Notice.objects.all()) > 0 else [],
        "invoice_count":Invoice.objects.filter(Q(lease__tenant__user=request.user) | Q(lease__leased_by=request.user)).count() if len(Invoice.objects.all()) > 0 else 0,

    }
    for val in vals:
        contexts[val.key] = val.value

    return contexts
