from django.urls import path
from .views import *

urlpatterns = [
    path('payment/create/', PaymentCreateView.as_view(), name='payment_create'),
    path('payment/mobile/', MobilePaymentView.as_view(), name='mobile_payment'),
    path('mpesa/callback/', MpesaCallbackView.as_view(), name='mpesa_callback'),
    path('mpesa/online/lipa', MobilePaymentView.as_view(), name='lipa_na_mpesa'),
    # path('payment/bank/<int:payment_id>/', BankPaymentView.as_view(), name='bank_payment'),
]
