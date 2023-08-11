from django.shortcuts import render, redirect
from django.views import View
from .models import Payment
from .forms import *
from django.contrib import messages
from django.urls import reverse_lazy
from .utils import MpesaPayment,CashPayment

class PaymentCreateView(View):
    template_name = 'payments/payment_create.html'
    form_class = PaymentForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Process payment based on payment method
            if form.cleaned_data['payment_method'] == 'cash':
                CashPayment(request).cashpay()  # Replace with your cash payment method
            elif  form.cleaned_data['payment_method'] == 'mobile':
                # Redirect to mobile payment page
                return redirect('mobile_payment', data=form.data)
            # elif form.cleaned_data['payment_method']  == 'bank':
            #     # Redirect to bank payment page
            #     return redirect('bank_payment')
            return redirect('invoice-list')

        return render(request, self.template_name, {'form': form})

class MobilePaymentView(View):
    template_name = 'payments/mobile_payment.html'  # Create this HTML template
    form_class = MpesaNumberForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={'mpesa_number': 254743793901})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            pass
        return render(request, self.template_name, {'form': form})