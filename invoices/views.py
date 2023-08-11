from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Invoice
from landlords.models import PropertyOwner,Agent
from django.contrib import messages
from .utils import InvoiceNumberGenerator

# Create an instance of the InvoiceNumberGenerator
invoice_number_generator = InvoiceNumberGenerator()
invoice_number = invoice_number_generator.generate_invoice_number()


class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'  # Update with your template path
    context_object_name = 'invoices'

    def get(self, request):
        invoices= Invoice.objects.all()
        if request.user.user_type == '4':
           invoices = invoices.filter(lease__tenant__user=request.user)
        elif request.user.is_superuser or (request.user_type != '1' and request.user_type == '2'):
               invoices = invoices
        return render(request, 'invoices/invoice_list.html', {'invoices':invoices})

class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoices/invoice_detail.html'  # Update with your template path
    context_object_name = 'invoice'

class InvoiceCreateView(CreateView):
    model = Invoice
    template_name = 'invoices/invoice_form.html'  # Update with your template path
    fields = ['lease', 'invoice_type', 'amount', 'description', 'due_date']
    success_url = reverse_lazy('invoice-list')

    def form_valid(self, form):
        invoice=form.instance
        invoice.invoice_id=invoice_number
        messages.success(self.request, 'Invoice created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to create invoice. Please check the form.')
        return super().form_invalid(form)

class InvoiceUpdateView(UpdateView):
    model = Invoice
    template_name = 'invoices/invoice_form.html'  # Update with your template path
    fields = ['lease', 'invoice_type', 'amount', 'description', 'due_date']
    context_object_name = 'invoice'
    success_url = reverse_lazy('invoice-list')

    def form_valid(self, form):
        messages.success(self.request, 'Invoice updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to update invoice. Please check the form.')
        return super().form_invalid(form)

class InvoiceDeleteView(DeleteView):
    model = Invoice
    template_name = 'invoices/invoice_confirm_delete.html'  # Update with your template path
    success_url = reverse_lazy('invoice-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Invoice deleted successfully.')
        return super().delete(request, *args, **kwargs)

