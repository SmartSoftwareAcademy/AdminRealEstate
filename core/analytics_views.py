# analytics_views.py

from django.shortcuts import render
from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField, Sum
from datetime import date
from tenants.models import *
from leases.models import *
from landlords.models import *
from payments.models import *
from property.models import *
from django.db.models import Q

def analytics_data(request):
    # get specific agents
    owner=PropertyOwner.objects.filter(user=request.user).first()
    agent=Agent.objects.filter(user=request.user).first()
    agents=None
    property_counts=None
    property_units=None
    total_tenants=None
    # get specifi tenats
    if owner:
        total_tenants = Tenant.objects.filter(created_by=owner.user).all()
        property_counts = Property.objects.filter(owner=owner).all()
        property_units=sum(property.units.count() for property in property_counts)
        agents=owner.agents.count()
    elif agent:
        total_tenants = Tenant.objects.filter(Q(created_by=agent) | Q(created_by__in=agent.owner.user))
        property_counts = Property.objects.filter(owner__agents__in=agent).all()
        property_units=sum(property.units.count() for property in property_counts)
    else:
        if request.user.is_superuser and (request.user_type != '1' and request.user_type == '2'):
            total_tenants=Tenant.objects.all()
    # Property Analysis
    property_types = Property.PROPERTY_TYPES
    total_properties =property_counts.count()
    property_counts=property_counts.values('property_type').annotate(count=Count('id'))
    rented_properties = Property.objects.filter(property_status='rented').count()
    total_properties_minus_rented_properties=total_properties-rented_properties
    occupancy_rate = (rented_properties / total_properties) * 100

    # Tenant Analysis
    gender_counts = total_tenants.values('user__gender').annotate(count=Count('id'))
    status_counts = total_tenants.values('current_status').annotate(count=Count('id'))

    # Lease Analysis
    lease_durations = Lease.objects.annotate(duration=ExpressionWrapper(F('end_date') - F('start_date'), output_field=DurationField()))
    average_duration = lease_durations.aggregate(avg_duration=Avg('duration'))
    median_duration = lease_durations.aggregate(median_duration=Avg('duration'))
    lease_start_dates = Lease.objects.values('start_date').annotate(count=Count('id'))
    upcoming_expirations = Lease.objects.filter(end_date__gte=date.today())

    # Payment Analysis
    rent_payments = Payment.objects.filter(description='rent_installment').order_by('date_paid')
    on_time_payments = Payment.objects.filter(date_paid__lte=F('lease__start_date')).count()
    total_payments = Payment.objects.count()
    total_payments_minus_on_time_payments=total_payments-on_time_payments
    if total_payments == 0:
        collection_rate = 0
    else:
        collection_rate = (on_time_payments / total_payments) * 100
    total_outstanding = Payment.objects.aggregate(total=Sum('outstanding_balance'))

    # Deposit Analysis
    deposit_amounts = RentDeposits.objects.values('amount').annotate(count=Count('id'))
    deposit_descriptions = RentDeposits.objects.values('description').annotate(count=Count('id'))

    context = {
        'page_title': "Administrative Dashboard",
        'property_types': property_types,
        'property_counts': property_counts,
        'total_agents': agents,
        'total_units': property_units,
        'total_properties': total_properties,
        'rented_properties': rented_properties,
        'occupancy_rate': occupancy_rate,
        'total_tenants': total_tenants.count(),
        'gender_counts': gender_counts,
        'status_counts': status_counts,
        'average_duration': average_duration,
        'median_duration': median_duration,
        'lease_start_dates': lease_start_dates,
        'upcoming_expirations': upcoming_expirations,
        'rent_payments': rent_payments,
        'on_time_payments': on_time_payments,
        'total_payments': total_payments,
        'collection_rate': collection_rate,
        'total_outstanding': total_outstanding,
        'deposit_amounts': deposit_amounts,
        'deposit_descriptions': deposit_descriptions,
        'total_properties_minus_rented_properties':total_properties_minus_rented_properties,
        'total_payments_minus_on_time_payments':total_payments_minus_on_time_payments,
    }
    return context
