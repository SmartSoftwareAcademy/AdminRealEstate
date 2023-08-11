import requests
from django.shortcuts import render, redirect
import json
from .models import *
from invoices.models import Invoice
from invoices.utils import *
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt
import time
from datetime import datetime
from core.utils import MailSender
from django.contrib import messages
import threading


payinfo=None
message = ""
msghead = ""
# @csrf_exempt

class MpesaPayment:
    def __init__(self,request):
        self.request=request
        self.payinfo=request.POST

    def lipa_na_mpesa_online(self):
        if self.request.method == 'POST':
            body_unicode=self.request.POST
            body = json.loads(body_unicode)
            print(body)
            global payinfo
            payinfo = body_unicode
            access_token = MpesaAccessToken.validated_mpesa_access_token
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            request = {
                "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
                "Password": LipanaMpesaPpassword.decode_password,
                "Timestamp": LipanaMpesaPpassword.lipa_time,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(float(body_unicode['amount'])),
                "PartyA": body_unicode['phone'],
                "PartyB": LipanaMpesaPpassword.Business_short_code,
                "PhoneNumber": body_unicode['phone'],
                "CallBackURL": "https://a159-154-159-237-65.in.ngrok.io/callback/",
                "AccountReference": "Fernbrook for %s" % body_unicode['invoice'],
                "TransactionDesc": "Fernbrook for %s" % body_unicode['invoice']
            }

            response = requests.post(api_url, json=request, headers=headers)
        # return HttpResponse({"CallBack Sent! ":response})
        global message
        global msghead
        if response:
            print(response)
            MailSender("Payment initiated", message+"\n\nPlease login to System to check the invoice.", ["titusowuor30@gmail.com",],[]).send_email()
            time.sleep(15)
        return redirect("display")


    @csrf_exempt
    def MpesaCallBack(self):
        try:
            data = self.request.body.decode('utf-8')
            print("callback sent:"+str(data))
            mpesa_payment = json.loads(data)
            print(mpesa_payment)
            print(mpesa_payment)
            result = 0
            global message
            global msghead
            if result == mpesa_payment['Body']['stkCallback']['ResultCode']:
                message = ""
                msghead = ""
                receivers = []
                receivers.append("info@tdbsoft.co.ke")
                receivers.append("titusowuor30@gmail.com")
                msghead = "Invoice Payment by {}".format(self.request.user.email)
                print(msghead)
                message = "Payment Made Successfully!\nTranasction #ID {}!".format(
                    payinfo['invoice'])
                print(message)
                self.SubmitToDB()
                if "email" in payinfo:
                    sendmail=MailSender(self.request,msghead+" "+self.payinfo['invoice'], "\n\nPlease login to System to check the invoice.", ["titusowuor30@gmail.com"],[]).send_email()
                    # Create a thread for the mail
                    thread = threading.Thread(target=sendmail)
                    # Set the thread as a daemon
                    thread.daemon = True
                    # Start the thread
                    thread.start()
                # if "sms" in payinfo:
                #     sendSMS(msghead, message,)
            else:
                message = ""
                msghead = ""
                msghead = "Failed!"
                print(msghead)
                print("Payment cancelled by user")
                message = "Request Failed!\nPayment cancelled by user!"
                displaymsg(self.request)
            return redirect('display')
        except Exception as e:
            print(e)


    def SubmitToDB(self):
        try:
            print(payinfo)
            invoice = Invoice.objects.get(invoice=payinfo['invoice'])
            print(invoice)
            if payinfo['amount'] == invoice.amount:
               invoice.status = "Paid"
            else:
                invoice.status = "Partial"
            invoice.save()
            displaymsg(self.request)
        except Exception as e:
            print(e)


def displaymsg(request):
    try:
        return render(request, "pages/result/payinfo.html", {'message': message, 'msghead': msghead})
    except Exception as e:
        print(e)

class CashPayment:
    def __init__(self,request):
        self.request=request
        self.payinfo=request.POST

    def cashpay(self):
        try:
            #print(self.payinfo)
            invoice = Invoice.objects.get(id=self.payinfo['invoice'])
            bal=float(invoice.balance)-float(self.payinfo['amount'])
            if bal == 0:
                invoice.status = "Paid"
                description=f"<h2>Payment of invoice #{self.payinfo['invoice']} in full!</h2>\
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
                            transaction_code=InvoiceNumberGenerator.generate_random_code(None),amount=float(self.payinfo['amount']),
                            description=description+"<p>"+self.payinfo['description']+"</p>",date_paid=datetime.now().date(),outstanding_balance=bal)
            payment.save()
            invoice.balance=bal
            invoice.save()
            sendmail=MailSender(self.request,msghead+" "+self.payinfo['invoice'], description+"<p style='color:red;'><br/><br/>Please note that this is a system generated email. Do not reply to this!</p>", invoice.lease.tenant.user.email,[]).send_email()
            # Create a thread for the mail
            thread = threading.Thread(target=sendmail)
            # Set the thread as a daemon
            thread.daemon = True
            # Start the thread
            thread.start()
            messages.success(self.request, 'Payment processed successfully.')
            displaymsg(self.request)
        except Exception as e:
            print(e)
