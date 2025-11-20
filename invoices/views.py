from datetime import date

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Invoice
from landlords.models import PropertyOwner, Agent
from leases.models import Lease
from django.contrib import messages
from .utils import InvoiceNumberGenerator
from staff.models import Staff

# Create an instance of the InvoiceNumberGenerator
invoice_number_generator = InvoiceNumberGenerator()
invoice_number = invoice_number_generator.generate_invoice_number()


class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'  # Update with your template path
    context_object_name = 'invoices'

    def get(self, request):
        invoices = Invoice.objects.all()
        if request.user.user_type == '4':
            invoices = invoices.filter(lease__tenant__user=request.user)
        elif request.user.is_superuser or (request.user.user_type != '1' or request.user.user_type == '2'):
            invoices = invoices
        # Optional overdue-only filter for tenants
        show_overdue = request.GET.get('overdue') == '1'
        if request.user.user_type == '4' and show_overdue:
            invoices = invoices.filter(due_date__lt=date.today()).exclude(status='Paid')
        # Maintenance invoice filter for Facility Managers
        show_maintenance = request.GET.get('maintenance') == '1'
        is_facility_manager = False
        if request.user.user_type == '3' and hasattr(request.user, 'staff'):
            role = (request.user.staff.position or '').lower()
            is_facility_manager = 'facility manager' in role
            if is_facility_manager and show_maintenance:
                invoices = invoices.filter(invoice_type='maintenance')
        context = {
            'invoices': invoices,
            'today': date.today(),
            'show_overdue': show_overdue,
            'show_maintenance': show_maintenance,
            'is_facility_manager': is_facility_manager,
        }
        return render(request, 'invoices/invoice_list.html', context)

class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoices/invoice_detail.html'  # Update with your template path
    context_object_name = 'invoice'

class InvoiceCreateView(CreateView):
    model = Invoice
    template_name = 'invoices/invoice_form.html'  # Update with your template path
    fields = ['lease', 'invoice_type', 'amount', 'description', 'due_date']
    success_url = reverse_lazy('invoice-list')

    def dispatch(self, request, *args, **kwargs):
        """
        Restrict invoice generation to Owners, Agents, Superusers,
        and Staff tagged as Property Manager.
        """
        user = request.user
        allowed = False
        if not user.is_authenticated:
            return redirect('login')
        if user.is_superuser or user.user_type in ('1', '2'):
            allowed = True
        elif user.user_type == '3' and hasattr(user, 'staff'):
            role = (user.staff.position or '').lower()
            if 'property manager' in role:
                allowed = True
        if not allowed:
            messages.error(request, "You are not allowed to generate invoices. Please contact the Property Manager.")
            return redirect('invoice-list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        invoice = form.instance
        # Auto-set invoice_id if not already set
        if not invoice.invoice_id:
            invoice.invoice_id = invoice_number
        # For rent invoices, default amount/balance from lease monthly rent when not provided
        if invoice.invoice_type == 'rent' and (not invoice.amount or invoice.amount == 0):
            invoice.amount = invoice.lease.monthly_rent
            invoice.balance = invoice.lease.monthly_rent
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


def lease_rent_amount(request, pk):
    """
    Lightweight JSON helper returning the monthly rent for a lease.
    Used by the invoice form to auto-fill rent invoices.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'Authentication required'}, status=401)
    lease = get_object_or_404(Lease, pk=pk)
    return JsonResponse({'monthly_rent': float(lease.monthly_rent)})

