from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *
from django.views.generic import CreateView,ListView,UpdateView,DeleteView,DetailView
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *

class StaffList(ListView):
    def get(self, request):
        staff=Staff.objects.all()
        return render(request, 'staff/staff_list.html', {'staff':staff})

class StaffCreate(CreateView):
    model=Staff
    form_class=StaffForm
    template_name="staff/staff_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items'] = StaffSalaryFormSet(self.request.POST, self.request.FILES,prefix="salary_set")
        else:
            context['items'] = StaffSalaryFormSet(prefix="salary_set")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        salary_formset = context['items']
        if salary_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.save()  # Save the staff instance to generate a primary key
            salary_instance = salary_formset.save(commit=False)
            salary_instance.staff = self.object
            salary_instance.save()

            salary_formset.save_m2m()  # Save many-to-many relationships
        return super().form_valid(form)

class StaffDetailView(DetailView):
    model = Staff
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(StaffDetailView, self).get_context_data(**kwargs)
        context["items"] = StaffSalary.objects.filter(staff=self.object)
        return context

class StaffUpdateView(LoginRequiredMixin, UpdateView):
    model = Staff
    fields = fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(StaffUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["items"] = StaffSalaryFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["items"] = StaffSalaryFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        itemsformset = context["items"]
        if form.is_valid() and itemsformset.is_valid():
            form.save()
            itemsformset.save()
        return super().form_valid(form)


class StaffDeleteView(LoginRequiredMixin, DeleteView):
    model = Staff
    success_url = reverse_lazy("staff-list")
