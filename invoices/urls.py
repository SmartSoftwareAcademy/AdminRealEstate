# urls.py

from django.urls import include, path
from django.urls import path
from .views import InvoiceListView, InvoiceDetailView, InvoiceCreateView, InvoiceUpdateView, InvoiceDeleteView

urlpatterns = [
    path('invoices/', InvoiceListView.as_view(), name='invoice-list'),
    path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoices/create/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('invoices/<int:pk>/update/', InvoiceUpdateView.as_view(), name='invoice-update'),
    path('invoices/<int:pk>/delete/', InvoiceDeleteView.as_view(), name='invoice-delete'),
]
