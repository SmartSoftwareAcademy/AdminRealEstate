from django.urls import path
from .views import *

urlpatterns = [
    path('staff-salary-payment/create/', StaffSalaryPaymentCreateView.as_view(), name='staff-salary-payment-create'),
    path('staff-salary-payment/list/', StaffSalaryPaymentListView.as_view(), name='staff-salary-payment-list'),
    path('staff-salary-payment/detail/<int:pk>/', StaffSalaryPaymentDetailView.as_view(), name='staff-salary-payment-detail'),
    path('staff-salary-payment/update/<int:pk>/', StaffSalaryPaymentUpdateView.as_view(), name='staff-salary-payment-update'),
    path('staff-salary-payment/payslip/<int:pk>/', PayslipPDFView.as_view(), name='payslip-pdf'),
]
