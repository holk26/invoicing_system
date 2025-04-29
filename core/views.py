from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib import messages
from core.models import (Invoice, Company, Client, Product, Tax, Note, OfflineQueue, 
                         AuditLog, User, InvoiceItem)
from core.forms import (CustomUserCreationForm, CompanyForm, ClientForm, ProductForm, 
                        TaxForm, InvoiceForm, InvoiceItemFormSet)
import zeep
import json
from django.http import JsonResponse
from django.views import View

def home_view(request):
    return render(request, 'home.html')

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('login')

class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'core/company_list.html'
    context_object_name = 'companies'

class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'core/company_form.html'
    success_url = reverse_lazy('company_list')

class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'core/company_form.html'
    success_url = reverse_lazy('company_list')

class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'core/company_confirm_delete.html'
    success_url = reverse_lazy('company_list')

class ClientListView(ListView):
    model = Client
    template_name = 'core/client_list.html'
    context_object_name = 'object_list'

class ClientCreateView(CreateView):
    model = Client
    fields = ['company', 'identification_type', 'identification_number', 'name', 'address', 'phone', 'email']
    template_name = 'core/client_form.html'
    success_url = reverse_lazy('client_list')

class ClientUpdateView(UpdateView):
    model = Client
    fields = ['company', 'identification_type', 'identification_number', 'name', 'address', 'phone', 'email']
    template_name = 'core/client_form.html'
    success_url = reverse_lazy('client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'core/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')

class ProductListView(ListView):
    model = Product
    template_name = 'core/product_list.html'

class ProductCreateView(CreateView):
    model = Product
    fields = ['company', 'code', 'description', 'price', 'tax', 'category', 'stock_quantity']
    template_name = 'core/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['company', 'code', 'description', 'price', 'tax', 'category', 'stock_quantity']
    template_name = 'core/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'core/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

class TaxListView(ListView):
    model = Tax
    template_name = 'core/tax_list.html'

class TaxCreateView(CreateView):
    model = Tax
    fields = ['tax_type', 'rate', 'description']
    template_name = 'core/tax_form.html'
    success_url = reverse_lazy('tax_list')

class TaxUpdateView(UpdateView):
    model = Tax
    fields = ['tax_type', 'rate', 'description']
    template_name = 'core/tax_form.html'
    success_url = reverse_lazy('tax_list')

class TaxDeleteView(DeleteView):
    model = Tax
    template_name = 'core/tax_confirm_delete.html'
    success_url = reverse_lazy('tax_list')

class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'core/invoice_list.html'
    context_object_name = 'invoices'

class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'core/invoice_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = InvoiceItemFormSet(self.request.POST)
        else:
            context['formset'] = InvoiceItemFormSet()
        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            # Simulate DIAN validation (RF05)
            xml_content = form.cleaned_data.get('xml_content', '')
            try:
                client = zeep.Client(wsdl='https://dian.gov.co/webservices')
                response = client.service.ValidateInvoice(xml_content=xml_content)
                cufe = response.get('CUFE', 'mock-cufe-123')
                digital_signature = response.get('Signature', 'mock-signature')
            except Exception:
                # Handle offline scenario (RF10)
                form.instance.status = 'offline'
                cufe = ''
                digital_signature = ''
                self.object = form.save()
                OfflineQueue.objects.create(
                    operation_type='create_invoice',
                    data=json.dumps({
                        'company': form.instance.company.id,
                        'client': form.instance.client.id,
                        'invoice_number': form.instance.invoice_number,
                        'total_amount': str(form.instance.total_amount),
                        'tax_amount': str(form.instance.tax_amount),
                        'discount_amount': str(form.instance.discount_amount),
                        'xml_content': xml_content,
                        'items': [
                            {
                                'product': item.product.id,
                                'quantity': item.quantity,
                                'unit_price': str(item.unit_price),
                                'tax_amount': str(item.tax_amount),
                                'subtotal': str(item.subtotal),
                            } for item in formset.cleaned_data
                        ]
                    }),
                    invoice=self.object
                )
            else:
                form.instance.cufe = cufe
                form.instance.digital_signature = digital_signature
                self.object = form.save()
            
            # Save formset
            formset.instance = self.object
            formset.save()
            
            # Log action (RNF13)
            AuditLog.objects.create(
                user=self.request.user,
                action='create_invoice',
                entity_type='invoice',
                entity_id=self.object.id,
                details=f'Created invoice {self.object.invoice_number}'
            )
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('invoice_list')

class InvoiceSyncView(LoginRequiredMixin, View):
    def post(self, request):
        offline_items = OfflineQueue.objects.filter(operation_type='create_invoice')
        for item in offline_items:
            try:
                data = json.loads(item.data)
                invoice = Invoice.objects.create(
                    company_id=data['company'],
                    client_id=data['client'],
                    invoice_number=data['invoice_number'],
                    total_amount=data['total_amount'],
                    tax_amount=data['tax_amount'],
                    discount_amount=data['discount_amount'],
                    xml_content=data['xml_content'],
                    status='pending'
                )
                for item_data in data['items']:
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        product_id=item_data['product'],
                        quantity=item_data['quantity'],
                        unit_price=item_data['unit_price'],
                        tax_amount=item_data['tax_amount'],
                        subtotal=item_data['subtotal']
                    )
                item.delete()
            except Exception:
                continue
        messages.success(request, 'Offline invoices synced successfully.')
        return redirect('invoice_list')

class ReportView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'core/report.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return Invoice.objects.filter(status='validated', issue_date__year=2025)