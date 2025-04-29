from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Custom User model for RF01, RF14
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('operator', 'Operator'),
        ('accountant', 'Accountant'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='operator')
    two_factor_enabled = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email

# Company model for RF02
class Company(models.Model):
    nit = models.CharField(max_length=50, unique=True)
    business_name = models.CharField(max_length=200)
    tax_regime = models.CharField(max_length=50)  # e.g., simplified, common
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    logo_path = models.CharField(max_length=200, blank=True)
    digital_certificate_path = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.business_name

# Product model for RF03
class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    tax = models.ForeignKey('Tax', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    stock_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.code} - {self.description}"

# Client model for RF09
class Client(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    identification_type = models.CharField(max_length=50)  # e.g., NIT, CC
    identification_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

# Tax model for RF15
class Tax(models.Model):
    tax_type = models.CharField(max_length=50)  # e.g., IVA, INC
    rate = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 19.00 for 19%
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tax_type} ({self.rate}%)"

# Invoice model for RF04, RF05, RF13
class Invoice(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('validated', 'Validated'),
        ('rejected', 'Rejected'),
        ('offline', 'Offline'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    xml_content = models.TextField(blank=True)  # XML UBL 2.1
    cufe = models.CharField(max_length=100, blank=True)  # Unique Electronic Invoice Code
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    digital_signature = models.TextField(blank=True)
    pdf_path = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.invoice_number

# Invoice Item model for RF04
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.product.description} (x{self.quantity})"

# Note model for RF13
class Note(models.Model):
    NOTE_TYPE_CHOICES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('validated', 'Validated'),
        ('rejected', 'Rejected'),
    )
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    note_type = models.CharField(max_length=20, choices=NOTE_TYPE_CHOICES)
    note_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    xml_content = models.TextField(blank=True)
    cufe = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    digital_signature = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.note_type} Note {self.note_number}"

# Audit Log model for RNF13
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)  # e.g., create_invoice
    entity_type = models.CharField(max_length=50)  # e.g., invoice
    entity_id = models.IntegerField()
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.action} by {self.user.email}"

# Offline Queue model for RF10
class OfflineQueue(models.Model):
    OPERATION_TYPE_CHOICES = (
        ('create_invoice', 'Create Invoice'),
        ('create_note', 'Create Note'),
    )
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, null=True, blank=True)
    operation_type = models.CharField(max_length=50, choices=OPERATION_TYPE_CHOICES)
    data = models.TextField()  # JSON serialized data
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.operation_type} (Queue ID: {self.id})"
