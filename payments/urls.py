from django.urls import path
from .views import *


urlpatterns = [
 # Rent Payment URLs
    path('rent-payment/create/', RentPaymentCreate.as_view(), name='rent-payment-create'),

]