from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import User, Company, Client, Product, Tax, Invoice, InvoiceItem

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'role', 'two_factor_enabled']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['nit', 'business_name', 'tax_regime', 'address', 'phone', 'email', 'logo_path', 'digital_certificate_path']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['company', 'identification_type', 'identification_number', 'name', 'address', 'phone', 'email']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['company', 'code', 'description', 'price', 'tax', 'category', 'stock_quantity']

class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = ['tax_type', 'rate', 'description']

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity', 'unit_price', 'tax_amount', 'subtotal']

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['company', 'client', 'invoice_number', 'total_amount', 'tax_amount', 'discount_amount', 'xml_content', 'status']

InvoiceItemFormSet = forms.inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=1,
    can_delete=True
)