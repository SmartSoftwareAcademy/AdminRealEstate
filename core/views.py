from django.shortcuts import render,redirect
from django.views import View
from tenants.models import *
from leases.models import *
from landlords.models import *
from payments.models import *
from property.models import *
from django.db.models import Q
from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField, Sum,Min,Max
from datetime import datetime
from django.views.generic import *
import re
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from .models import Setup
from django.contrib import messages
from django.urls import reverse_lazy
from .models import *
from notices.models import Enquiries
from notices.forms import EnquirytForm
from notices.models import Notice
from invoices.models import Invoice
from .forms import *
from django.db.models import Sum, F
from datetime import datetime
from .utils import tenant_rent_analytics,get_rent_payment_analytics

User=get_user_model()

class Home(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
       # get specific agents
        owner=PropertyOwner.objects.filter(user=request.user).first()
        agent=Agent.objects.filter(user=request.user).first()
        agents=None
        property_counts=None
        property_units=None
        total_tenants=None
        # get specifi tenats
        if owner:
            print(agent)
            total_tenants = Tenant.objects.filter(Q(created_by=owner.user) | Q(leases__property_unit__unit_code__in=[o.units.values('unit_code') for o in owner.properties.all()])).distinct()
            property_counts = Property.objects.filter(owner=owner).all()
            property_units=sum(property.units.count() for property in property_counts)
            agents=owner.agents.count()
        elif agent:
            total_tenants = Tenant.objects.filter(Q(created_by=agent.user) | Q(leases__property_unit__unit_code__in=[a.units.values('unit_code') for a in agent.owner.properties.all()])).distinct()
            print(agent)
            property_counts = Property.objects.filter(owner__agents=agent).all()
            property_units=sum(property.units.count() for property in property_counts)
        else:
            if request.user.is_superuser or (request.user.user_type != '1' or request.user.user_type == '2'):
                total_tenants=Tenant.objects.all()
        # Property Analysis
        property_types = sorted(Property.PROPERTY_TYPES)
        total_properties =property_counts.count() if property_counts else 0
        property_type_counts=property_counts.values('property_type').annotate(count=Count('id')).order_by('property_type') if property_counts else []
        # Create a dictionary to store the counts
        property_type_count_dict = {property_type[0]: 0 for property_type in property_types}
        # Update the counts with the actual values
        for property_type_count in property_type_counts:
            property_type = property_type_count['property_type']
            count = property_type_count['count']
            property_type_count_dict[property_type] = count
        # Create a list of property type counts
        property_type_count_list = [property_type_count_dict[property_type[0]] for property_type in property_types]
        rented_properties = Property.objects.filter(property_status='rented').count()
        available_properties=total_properties-rented_properties
        occupancy_rate = (rented_properties / total_properties) * 100 if total_properties > 0 else 0.00

        # Tenant Analysis
        gender_counts = total_tenants.values('user__gender').annotate(count=Count('id')).order_by('user__gender')
        gender_count_labels=['Female' if 'F' in label['user__gender'] else 'Male'  for label in gender_counts]
        gender_count_data=[d['count'] for d in gender_counts]
        active_counts = total_tenants.values('current_status').filter(current_status='active').count()
        inactive_counts = total_tenants.values('current_status').filter(current_status='inactive').count()

        # Lease Analysis
        lease=Lease.objects.filter(Q(leased_by=request.user))
        average_duration,median_duration=0,0
        lease_start_dates_lables=[]
        exp_labels=[]
        exp_data=[]
        lease_start_dates=None
        upcoming_expirations=[]
        lease_start_dates_data=[]
        if len(lease) > 0:
            lease_durations = lease.annotate(duration=ExpressionWrapper(F('end_date') - F('start_date'), output_field=DurationField()))
            average_duration = lease_durations.aggregate(avg_duration=Avg('duration'))['avg_duration'].days
            median_duration = lease_durations.aggregate(median_duration=Avg('duration'))['median_duration'].days
            lease_start_dates =lease.values('start_date').annotate(count=Count('id'))
            lease_start_dates_lables=[datetime.strptime(str(d['start_date']), "%Y-%m-%d").strftime("%m-%d-%Y") for d in lease_start_dates]
            lease_start_dates_data=[d['count'] for d in lease_start_dates]
            upcoming_expirations = lease.filter(end_date__gte=date.today())
            exp_labels=[datetime.strptime(str(d.end_date), "%Y-%m-%d").strftime("%m-%d-%Y") for d in upcoming_expirations]
            exp_data=[f"{d.tenant.user.username}-{d.property_unit.unit_code}" for d in upcoming_expirations]

        # Payment Analysis
        on_time_payments=0
        rent_payments=[]
        total_payments=0
        collection_rate=0
        total_outstanding=2000
        late_payments=0
        actual_rent_paid, actual_rent_owed=0,0
        rent_payments=Payment.objects.all()
        if len(rent_payments) > 0:
            rent_payments = rent_payments.filter(invoice__invoice_type='rent').order_by('date_paid')
            #print(rent_payments)
            on_time_payments = rent_payments.filter(date_paid__lte=F('invoice__lease__start_date')).count()
            total_payments = rent_payments.count()
            late_payments=total_payments-on_time_payments
            if total_payments == 0:
                collection_rate = 0
            else:
                collection_rate = (on_time_payments / total_payments) * 100
            total_outstanding = rent_payments.values("invoice__balance","invoice__amount","invoice__lease__tenant").distinct().aggregate(total=Sum('invoice__balance'))['total']
        #print("outstanding=>",total_outstanding)
        if request.user.user_type=='4':
           actual_rent_paid, actual_rent_owed = tenant_rent_analytics(request.user)

        #yearly by month rent analytics
        year = int(request.GET.get('year', datetime.now().year))
        analytics = get_rent_payment_analytics(year)
        months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"]
        month_totals=[]
        for i in analytics:
            month_totals.append(float(i['total_payments']))
        #print(months,month_totals)

        # Deposit Analysis
        # Calculate average, minimum, maximum, and total security deposit amounts
        deposit_data=[1000,10,10,10]
        if len(Lease.objects.all())>0:
            average_security_deposit = Lease.objects.aggregate(Avg('security_deposit'))['security_deposit__avg']
            minimum_security_deposit = Lease.objects.aggregate(Min('security_deposit'))['security_deposit__min']
            maximum_security_deposit = Lease.objects.aggregate(Max('security_deposit'))['security_deposit__max']
            total_security_deposit = Lease.objects.aggregate(Sum('security_deposit'))['security_deposit__sum']
            deposit_data=[float(f"{minimum_security_deposit:.2f}"),float(f"{maximum_security_deposit:.2f}"),float(f"{average_security_deposit:.2f}"),float(f"{total_security_deposit:.2f}")]
        #print("====>",deposit_data)
        context = {
            'page_title': "Administrative Dashboard",
            'property_types': property_types,
            'property_counts': property_type_count_list,
            'total_agents': agents,
            'total_units': property_units,
            'total_properties': total_properties,
            'rented_properties': rented_properties,
            'occupancy_rate': occupancy_rate,
            'total_tenants': total_tenants.count(),
            'gender_count_labels': gender_count_labels,
            'gender_count_data':gender_count_data,
            'active_counts': active_counts,
            'inactive_counts': inactive_counts,
            'average_duration': average_duration,
            'median_duration': median_duration,
            'lease_start_dates_lables': lease_start_dates_lables,
            'lease_start_dates_data': lease_start_dates_data,
            'upcoming_expirations': upcoming_expirations,
            'exp_labels': exp_labels,
            'exp_data': exp_data,
            'rent_payments': rent_payments,
            'on_time_payments': on_time_payments,
            'total_payments': total_payments,
            'collection_rate': collection_rate,
            'total_outstanding': total_outstanding,
            'deposit_data':deposit_data,
            'available_properties':available_properties,
            'late_payments':late_payments,
            'actual_rent_paid': actual_rent_paid,
            'actual_rent_owed': actual_rent_owed,
            'months': months,
            'month_totals': month_totals,
        }
        return render(request,"core/index.html",context)

def hide_welcome(request):
    pk=int(request.POST['pk'])
    note=Notice.objects.get(id=pk)
    note.read=True
    note.save()
    messages.success(request,"Notice marked as read!")
    return redirect('home')

class FrontPage(ListView):
    def get(self, request):
        # get specifi tenats
        properties = Property.objects.all()
        featured_properties = Property.objects.filter(is_featured=True)
        featured_units=Units.objects.filter(is_featured=True).distinct()
        agents=Agent.objects.filter(Q(owner__properties__property_name__icontains=get_site_name(self.request)))
        testimonials=Testimonial.objects.filter(Q(published=True))#& Q(property__property_name__icontains=get_site_name(self.request)
        services=Services.objects.filter(Q(published=True) & Q(property__property_name__icontains=get_site_name(self.request)))

        context= {'properties':properties,
                  'featured_properties':featured_properties,
                  'featured_units':featured_units,
                  "site_agents":agents,
                  "testimonials":testimonials,
                  "services":services,
                  }
        return render(request, 'core/frontpage.html',context)

def get_site_name(request):
    configs=SiteConfig.objects.all()
    return str(configs[0].value)


class PropertyDetailView(DetailView):
    model = Property
    template_name = 'core/property-detail.html'
    context_object_name = 'property'

class UnitDetailView(DetailView):
    model = Units
    template_name = 'core/unit-detail.html'
    context_object_name = 'unit'



class PropertyPage(ListView):
    model = Property
    template_name = 'core/properties.html'
    context_object_name = 'properties'

    def get(self, request):
        # get specifi tenats
        properties=Property.objects.all()
        featured_properties = Property.objects.filter(is_featured=True).all()
        return render(request, 'core/properties.html', {'featured_properties':featured_properties,"site_properties":properties})

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        address = self.request.GET.get('address')
        city = self.request.GET.get('city')

        if name:
            queryset = queryset.filter(property_name__icontains=name)
        if address:
            queryset = queryset.filter(address__icontains=address)
        if city:
            queryset = queryset.filter(city__icontains=city)

        print(queryset)

        return queryset

class ServicePage(ListView):
    def get(self, request):
        testimonials=Testimonial.objects.filter(Q(published=True) & Q(property__property_name__icontains=get_site_name(self.request)))
        services=Services.objects.filter(Q(published=True) & Q(property__property_name__icontains=get_site_name(self.request)))
        context= {'services':services,
                  'testimonials':testimonials,
                  }
        return render(request, 'core/services.html',context)

class AbouttPage(View):
    def get(self, request):
        about_content=About.objects.filter(Q(published=True) & Q(property__property_name__icontains=get_site_name(self.request))).first()
        agents=Agent.objects.filter(Q(owner__properties__property_name__icontains=get_site_name(self.request)))
        return render(request, 'core/about.html', {'about_content':about_content,'site_agents':agents})

class ContactPage(View):
    def get(self, request):
        form=EnquirytForm()
        return render(request, 'core/contact.html', {'form':form,'about':[]})

    def post(self,request):
        form = EnquirytForm(request.POST)
        if form.is_valid():
            enquiry=form.save()
            messages.success(request,'Your Message has been submitted to our capable helpdesk tean, we will get back to you as soon as possible!')
        return redirect('frontpage')  # Redirect to the same form page after successful submission

class TestimonyView(View):
    def get(self, request):
        return render(request, 'core/contact.html', {'about':[]})


class TestimonialCreateView(CreateView):
    def get(self, request):
        form = TestimonialForm()
        return render(request,  'core/testimonial.html', {'form': form})

    def post(self, request):
        form = TestimonialForm(request.POST)
        if form.is_valid():
            property_id=Property.objects.filter(Q(property_name__icontains=get_site_name(self.request))).first()
            testimonial=form.save(commit=False)
            testimonial.user=request.user
            testimonial.property=property_id
            testimonial.save()
            messages.success(request,'Testimonial submitted for review successfully!')
            return redirect('frontpage')  # Redirect to the same form page after successful submission
