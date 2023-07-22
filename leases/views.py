from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Lease, LeaseTerm
from django.views.generic import CreateView,ListView,UpdateView,DeleteView,DetailView
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LeaseForm, LeaseTermFormset
from landlords.models import *

class LeaseList(ListView):
    def get(self, request):
        owner=PropertyOwner.objects.filter(user=request.user).first()
        agent=Agent.objects.filter(user=request.user).first()
        leases= leases = Lease.objects.all()
        if owner:
           leases = leases.filter(leased_by=owner.user).all()
        elif agent:
            leases =leases.filter(leased_by=agent)
        else:
            if request.user.is_superuser and (request.user_type != '1' and request.user_type == '2'):
               leases = leases
        return render(request, 'leases/lease_list.html', {'leases':leases})

class LeaseListCreate(CreateView):
    model=Lease
    form_class=LeaseForm
    template_name="leases/lease_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items'] = LeaseTermFormset(self.request.POST, self.request.FILES,prefix="term_set")
        else:
            context['items'] = LeaseTermFormset(prefix="term_set")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        term_formset = context['items']
        with transaction.atomic():
            self.object = form.save()
            if term_formset.is_valid():
                term_formset.instance = self.object
                term_formset.save()
        return super().form_valid(form)

class LeaseDetailView(DetailView):
    model = Lease
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(LeaseDetailView, self).get_context_data(**kwargs)
        context["items"] = LeaseTerm.objects.filter(lease=self.object)
        return context

class LeaseUpdateView(LoginRequiredMixin, UpdateView):
    model = Lease
    fields = fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(LeaseUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["items"] = LeaseTermFormset(
                self.request.POST, instance=self.object
            )
        else:
            context["items"] = LeaseTermFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        itemsformset = context["items"]
        if form.is_valid() and itemsformset.is_valid():
            form.save()
            itemsformset.save()
        return super().form_valid(form)


class LeaseDeleteView(LoginRequiredMixin, DeleteView):
    model = Lease
    success_url = reverse_lazy("lease-list")
