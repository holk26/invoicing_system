from django.urls import path
from core.views import (
    RegisterView, CompanyListView, CompanyCreateView, ClientListView, ClientCreateView,
    ProductListView, ProductCreateView, TaxListView, TaxCreateView, InvoiceListView,
    InvoiceCreateView, InvoiceSyncView, ReportView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('companies/add/', CompanyCreateView.as_view(), name='company_add'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/add/', ClientCreateView.as_view(), name='client_add'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('taxes/', TaxListView.as_view(), name='tax_list'),
    path('taxes/add/', TaxCreateView.as_view(), name='tax_add'),
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/add/', InvoiceCreateView.as_view(), name='invoice_add'),
    path('invoices/sync/', InvoiceSyncView.as_view(), name='invoice_sync'),
    path('reports/', ReportView.as_view(), name='report'),
]