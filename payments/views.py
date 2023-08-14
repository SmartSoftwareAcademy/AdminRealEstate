from django.views import View
from invoices.models import Invoice
from .forms import *
from django.contrib import messages
from django.urls import reverse
from .utils import CashPayment
from urllib.parse import urlencode
import json
from django.views import View
import requests
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.http import HttpResponse
from .models import *
from invoices.models import Invoice
from invoices.utils import *
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import time
from core.utils import MailSender
import threading

payinfo=None
message = ""
msghead = ""

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
                data = {'amount': form.cleaned_data['amount'], 'invoice_id':request.POST['invoice'],'description':form.cleaned_data['description']}
                query_string = urlencode(data)
                url = reverse('mobile_payment') + '?' + query_string
                return redirect(url)
            # elif form.cleaned_data['payment_method']  == 'bank':
            #     # Redirect to bank payment page
            #     return redirect('bank_payment')
            return redirect('invoice-list')

        return render(request, self.template_name, {'form': form})

class MobilePaymentView(View):
    template_name = 'payments/mobile_payment.html'  # Create this HTML template
    form_class = MpesaNumberForm

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        print(request.GET.get('invoice_id'))
        invoice=Invoice.objects.get(id=int(request.GET.get('invoice_id')))
        form = self.form_class(initial={'mpesa_number': 254743793901,'amount':request.GET.get('amount'),'invoice_id':invoice.invoice_id,'description':request.GET.get('description')})
        return render(request, self.template_name, {'form': form,'amount':request.GET.get('amount'),'invoice_id':invoice.invoice_id})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            body_data = form.cleaned_data  # Use cleaned_data instead of data for form data

            try:
                invoice = Invoice.objects.get(invoice_id=body_data['invoice_id'])
            except Invoice.DoesNotExist:
                return JsonResponse({'message': 'Invoice not found'}, status=400)

            access_token = MpesaAccessToken.validated_mpesa_access_token
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            request_data = {
                "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
                "Password": LipanaMpesaPpassword.decode_password,
                "Timestamp": LipanaMpesaPpassword.lipa_time,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(float(body_data['amount'])),
                "PartyA": body_data['mpesa_number'],
                "PartyB": LipanaMpesaPpassword.Business_short_code,
                "PhoneNumber": body_data['mpesa_number'],
                "CallBackURL": "https://dddc-105-161-138-19.ngrok-free.app/payments/mpesa/callback/",
                "AccountReference": f"Fernbrook Apartments for Rent Invoice #{invoice.invoice_id}",
                "TransactionDesc": f"Fernbrook Apartments for Rent Invoice #{invoice.invoice_id}"
            }

            response = requests.post(api_url, json=request_data, headers=headers)
            if response.status_code == 200:
                # Payment request sent successfully
                return JsonResponse({'message':'Accepted' },status=200)
            else:
                return JsonResponse({'message': 'Failed to submit payment request'}, status=500)

        return JsonResponse({'message': 'Invalid form data'}, status=400)

class MpesaCallbackView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            data = self.request.body.decode('utf-8')
            print("callback sent:"+str(data))
            mpesa_payment = json.loads(data)
            print(mpesa_payment)
            result = 0
            global message
            global msghead
            global payinfo
            if result == mpesa_payment['Body']['stkCallback']['ResultCode']:
                message = ""
                msghead = ""
                print(payinfo)
                invoice = Invoice.objects.get(id=payinfo['invoice_id'])
                bal=float(invoice.balance)-float(payinfo['amount'])
                if bal == 0:
                    invoice.status = "Paid"
                    description=f"<h2>Payment of invoice #{payinfo['invoice']} in full!</h2>\
                        <h3>Invoice Details</h3>\
                        <p><b>Invoice ID</b>:{invoice.invoice_id}</p>\
                        <p><b>Invoice Amount</b>:{invoice.amount}</p>\
                        <p><b>Balance</b>:{bal}</p>\
                        <p><b>Due Date</b>:{invoice.due_date}</p>"
                else:
                    invoice.status = "Partial"
                    description=f"<h2 style='color:green;'>Payment of invoice #{invoice.invoice_id} partially!</h2>\
                        <h3>Invoice Details</h3>\
                        <p><b>Invoice ID</b>:{invoice.invoice_id}</p>\
                        <p><b>Invoice Amount</b>:{invoice.amount}</p>\
                        <p><b>Balance</b>:{bal}</p>\
                        <p><b>Due Date</b>:{invoice.due_date}</p>"
                payment=Payment(invoice=invoice,payment_method='cash',
                                transaction_code=InvoiceNumberGenerator.generate_random_code(None),amount=float(payinfo['amount']),
                                description=description+"<p>"+payinfo['description']+"</p>",date_paid=datetime.now().date(),outstanding_balance=bal)
                payment.save()
                invoice.balance=bal
                invoice.save()
                sendmail=MailSender(self.request,msghead+" "+payinfo['invoice'], description+"<p style='color:red;'><br/><br/>Please note that this is a system generated email. Do not reply to this!</p>", invoice.lease.tenant.user.email,[]).send_email()
                # Create a thread for the mail
                thread = threading.Thread(target=sendmail)
                # Set the thread as a daemon
                thread.daemon = True
                # Start the thread
                thread.start()
                return JsonResponse({'success': True},status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'success': False},status=500)
        return JsonResponse({'success': False},status=400)
