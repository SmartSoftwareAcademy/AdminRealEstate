from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.db import transaction
from .models import *
from .forms import *
from landlords.models import *

class PropertyList(View):
    def get(self, request):
        owner=PropertyOwner.objects.filter(user=request.user).first()
        agent=Agent.objects.filter(user=request.user).first()
        properties=None
        # get specifi tenats
        if owner:
            properties = Property.objects.filter(owner=owner).all()
        elif agent:
            properties = Property.objects.filter(owner__agents=agent).all()
        else:
            if request.user.is_superuser and (request.user.user_type != '1' or request.user.user_type == '2'):
                properties=Property.objects.all()
        return render(request, 'property/property_list.html', {'properties':properties})


class PrpertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'property/property_form.html'
    success_url = reverse_lazy('property-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = PropertyImagesFormSet(self.request.POST, self.request.FILES,prefix="image_set")
        else:
            data['items'] = PropertyImagesFormSet(prefix="image_set")
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['items']
        with transaction.atomic():
            self.object = form.save(commit=False)
            owner=PropertyOwner.objects.filter(agents__user=self.request.user).first()
            self.object.owner=owner
            if image_formset.is_valid():
                image_formset.instance = self.object
                image_formset.save()
        return super().form_valid(form)


class PropertyDetailView(LoginRequiredMixin, DetailView):
    model = Property
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(PropertyDetailView, self).get_context_data(**kwargs)
        context["items"] = PropertyImages.objects.filter(property=self.object)
        return context


class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    fields = fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(PropertyUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["items"] = PropertyImagesFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["items"] = PropertyImagesFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        itemsformset = context["items"]
        if form.is_valid() and itemsformset.is_valid():
            form.save()
            itemsformset.save()
        return super().form_valid(form)



class PropertyDeleteView(LoginRequiredMixin, DeleteView):
    model = Property
    success_url = reverse_lazy("property-list")
