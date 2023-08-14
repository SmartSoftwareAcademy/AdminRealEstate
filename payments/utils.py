from .models import *
from invoices.models import Invoice
from invoices.utils import *
from datetime import datetime
from core.utils import MailSender
from django.contrib import messages
import threading

payinfo=None
message = ""
msghead = ""

class CashPayment:
    def __init__(self,request):
        self.request=request
        self.payinfo=request.POST

    def cashpay(self):
        try:
            print(self.payinfo)
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
        except Exception as e:
            print(e)
