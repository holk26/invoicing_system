from django.contrib import admin
from core.models import User, Company, Client, Product, Tax, Invoice, InvoiceItem, Note, OfflineQueue, AuditLog

admin.site.register([User, Company, Client, Product, Tax, Invoice, InvoiceItem, Note, OfflineQueue, AuditLog])