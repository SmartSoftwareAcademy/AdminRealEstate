from django.forms.models import BaseModelForm
from django.shortcuts import render,redirect
from django.views.generic import CreateView,ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import datetime
import io
from django.http import FileResponse
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from .models import StaffSalaryPayment
from .forms import StaffPaymentForm
from core.models import Setup,SiteConfig
from staff.models import StaffSalary,Staff
# Create your views here.
from django.contrib import messages
from pathlib import Path
from django.contrib.sites.models import Site
from reportlab.lib.units import inch


class StaffSalaryPaymentCreateView(CreateView):
    model = StaffSalaryPayment
    form_class = StaffPaymentForm
    template_name = 'payments/payroll.html'
    success_url = reverse_lazy('staff-salary-payment-list')

    def form_valid(self, form):
        print(form.cleaned_data['staff'])
        payment=form.save(commit=False)
        staff_email=form.cleaned_data['staff']
        staff=Staff.objects.filter(user__email=staff_email).first()
        staff_salary=StaffSalary.objects.filter(staff=staff).first()
        if staff_salary == None:
            messages.warning(self.request,f"No Salary Details found for {staff_email}!\nPlease consider adding it first then retry payment!",extra_tags='warning')
            return redirect('staff-update',staff.id)
        payment.net_pay=staff_salary.net_salary
        payment.save()
        return super().form_valid(form)

class StaffSalaryPaymentListView(ListView):
    model = StaffSalaryPayment
    template_name = 'payments/payroll-list.html'
    context_object_name = 'staff_payments'

class StaffSalaryPaymentDetailView(DetailView):
    model = StaffSalaryPayment
    template_name = 'payments/payroll-detail.html'
    context_object_name = 'staff_payment'

class StaffSalaryPaymentUpdateView(UpdateView):
    model = StaffSalaryPayment
    form_class = StaffPaymentForm
    template_name = 'payments/payroll.html'
    context_object_name = 'staff_payment'
    success_url = reverse_lazy('staff-salary-payment-list')


class PayslipPDFView(View):

    def get(self, request, *args, **kwargs):
        self.configs=SiteConfig.objects.all()
        self.site_setup=Setup.objects.first()

        try:
           staff_salary_payment = StaffSalaryPayment.objects.get(id=self.kwargs['pk'])
        except StaffSalaryPayment.DoesNotExist:
            return HttpResponse("Staff Salary Payment not found.", status=404)

        doc = SimpleDocTemplate("payslip.pdf", pagesize=letter)
        styles = getSampleStyleSheet()

        # Create a list to hold the contents of the payslip
        payslip_content = []

        # Add the page header
        header=self.get_header_text()
        header_style = styles['Heading2']
        header_style.vAlign=1
        footer_style = styles['Normal']
        footer_style.alignment = 1
        footer_style.vAlign = 2
        # Align the text to the right
        # Create a list to hold the elements of the PDF document.
        # Add the school logo and details to the header.
        logo_path =self.get_site_url()+self.site_setup.logo.url if self.site_setup.logo else finders.find('dist/img/logo.png')
        logo = Image(logo_path, width=100, height=100)
        header_text=Paragraph(header, header_style)
        logo.hAlign = 'LEFT'
        # Create a table to hold the logo and header text side by side
        header_table = Table([[logo, header_text]], colWidths=[120, None])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertically align the logo and header text
            ('ALIGN', (0, 0), (-1, -1), 'CENTRE'),  # Horizontally align the logo and header text
        ]))

        payslip_content.extend([header_table, Spacer(20, 20)])

        # Add the payslip title
        title = Paragraph("Staff Payslip", styles["Title"])
        payslip_content.append(title)

        # Add staff details
        staff_details = [
            ["Staff Name:                ------------------------------------", staff_salary_payment.staff.user.get_full_name()],
            ["Month:                        ------------------------------------", staff_salary_payment.month],
            ["Year:                           ------------------------------------", staff_salary_payment.year],
            ["Date of Payment:       ------------------------------------",datetime.fromisoformat(str(staff_salary_payment.date_of_pyament)).strftime("%Y-%m-%d") ],
        ]
        staff_table = Table(staff_details, colWidths=250, rowHeights=30)
        staff_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
        ]))
        payslip_content.append(staff_table)

        # Add earnings and deductions details
        salary_details = staff_salary_payment.staff.salary_details.all()

        if salary_details:
            payslip_content.append(Paragraph("Earnings:", styles["Heading3"]))
            for earning in [e.earnings.all() for e in salary_details][0]:
                payslip_content.append(Paragraph(f"{earning.name}: {earning.amount}", styles["Normal"]))

            payslip_content.append(Paragraph("Deductions:", styles["Heading3"]))
            for deduction in [d.deductions.all() for d in salary_details][0]:
                payslip_content.append(Paragraph(f"{deduction.name}: {deduction.amount}", styles["Normal"]))

        # Add net pay
        payslip_content.append(Paragraph(f"Net Pay: {staff_salary_payment.net_pay}", styles["Heading3"]))
        payslip_content.append(Paragraph("<br /><br />Employer's Signature &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Employee's Signature", header_style))
        payslip_content.append(Paragraph("<br/>............................ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ..........................", header_style))


        # Add the page header
        #footer_text=self.get_footer()
        #payslip_content.append(Paragraph(footer_text,footer_style))

        # Build the PDF
        doc.build(payslip_content,onFirstPage=self.add_footer, onLaterPages=self.add_footer)
        # Return the generated PDF as a response
        with open(f"payslip.pdf", "rb") as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type="application/pdf")
            response["Content-Disposition"] = f"inline; filename=payslip_{timezone.now().day}.pdf"
            return response

    def get_site_url(self):
        if self.request:
            # Get the protocol and domain from the request
            site_protocol = 'https' if self.request.is_secure() else 'http'
            site_domain = self.request.get_host()

            # Combine the protocol and domain to get the site URL
            site_url = f"{site_protocol}://{site_domain}"
        else:
            # If request is not available (e.g., in production),
            # get the domain from the Site model
            current_site = Site.objects.get_current()
            site_domain = current_site.domain
            site_url = f"http://{site_domain}"

        return site_url

    def get_header_text(self):
        text=f"{self.configs[0].value}<br />{self.configs[2].value}\
        <br />{self.configs[1].value}<br />{self.configs[3].value}\
        <br />{self.configs[4].value}"
        return text

    def add_footer(self,canvas, doc):
        # Footer text
        footer_text = f"Payslip generated by {self.request.user.email}     @ {timezone.now().year} Real Estate Admin           Date: " + str(timezone.now())
        # Get the page size
        page_width, page_height = letter
        # Draw the footer text at the bottom of the page
        canvas.saveState()
        canvas.setFont("Helvetica", 10)
        canvas.drawCentredString(page_width / 2, inch, footer_text)
        canvas.restoreState()