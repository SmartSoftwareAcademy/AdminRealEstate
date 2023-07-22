from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import *
from .models import *
# Rent Payment views
class RentPaymentCreate(View):
    def get(self, request):
        form = RentPaymentForm()
        return render(request, 'rent_payments/rent_payment_create.html', {'form': form})

    def post(self, request):
        form = RentPaymentForm(request.POST)
        if form.is_valid():
            rent_payment = form.save()
            return redirect(rent_payment)
        return render(request, 'rent_payments/rent_payment_create.html', {'form': form})