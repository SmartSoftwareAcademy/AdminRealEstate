from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import transaction
from django.db.models import Q
from .models import *
from landlords.models import *
from .forms import *

class TenatList(View):
    def get(self, request):
       # get specific agents
        owner=PropertyOwner.objects.filter(user=request.user).first()
        agent=Agent.objects.filter(user=request.user).first()
        tenants=None
        # get specifi tenats
        if owner:
            tenants = Tenant.objects.filter(created_by=owner.user).all()
        elif agent:
            tenants = Tenant.objects.filter(Q(created_by=agent) | Q(created_by__in=agent.owner.user))
        else:
            if request.user.is_superuser and (request.user_type != '1' and request.user_type == '2'):
                tenants=Tenant.objects.all()
        return render(request, 'tenants/tenant_list.html', {'tenants':tenants})


class TenantCreateView(LoginRequiredMixin, CreateView):
    model = Tenant
    form_class = TenantForm
    template_name = 'tenants/tenant_form.html'
    success_url = reverse_lazy('tenant-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = TenantKinFormSet(self.request.POST, self.request.FILES,prefix="kin_set")
        else:
            data['items'] = TenantKinFormSet(prefix="kin_set")
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        kin_formset = context['items']
        with transaction.atomic():
            user_data = {
                'email': form.cleaned_data['email'],
                'gender': form.cleaned_data['gender'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'other_name': form.cleaned_data['other_name'],
                'address': form.cleaned_data['address'],
            }
            profile_pic = form.cleaned_data['profile_pic']
            if profile_pic:
                # Save the profile picture to a temporary file
                temp_file = NamedTemporaryFile(delete=True)
                temp_file.write(profile_pic.read())
                temp_file.flush()

                # Create a File object from the temporary file
                profile_pic_file = File(temp_file)

                # Assign the File object to the user's profile_pic field
                user_data['profile_pic'] = profile_pic_file

            user = get_user_model().objects.create_user(**user_data)
            self.object = form.save(commit=False)
            self.object.user = user
            self.object.created_by=self.request.user
            self.object.save()
            if kin_formset.is_valid():
                kin_formset.instance = self.object
                kin_formset.save()
        return super().form_valid(form)


class TenantDetailView(LoginRequiredMixin, DetailView):
    model = Tenant
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(TenantDetailView, self).get_context_data(**kwargs)
        context["items"] = Tenant_Kin.objects.filter(tenant=self.object)
        return context


class TenantUpdateView(LoginRequiredMixin, UpdateView):
    model = Tenant
    form_class = TenantForm
    template_name = 'tenants/tenant_form.html'
    #success_url = reverse_lazy('tenant-detail')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = TenantKinFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object,
                prefix="kin_set"
            )
        else:
            data['items'] = TenantKinFormSet(instance=self.object, prefix="kin_set")
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['items']
        with transaction.atomic():
            self.object = form.save(commit=False)
            user = self.object.user  # Retrieve the existing user associated with the Tenant
            user.email = form.cleaned_data['email']
            user.gender = form.cleaned_data['gender']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.other_name = form.cleaned_data['other_name']
            user.address = form.cleaned_data['address']
            profile_pic = form.cleaned_data['profile_pic']
            if profile_pic:
                user.profile_pic = profile_pic
            user.save()
            self.object.created_by=self.request.user
            self.object.save()
            if image_formset.is_valid():
                image_formset.save()
        return super().form_valid(form)



class TenantDeleteView(LoginRequiredMixin, DeleteView):
    model = Tenant
    success_url = reverse_lazy("tenant-list")
