from django.urls import path, include
from .views import (
    home_view,
    RegisterView,
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    TaxListView, TaxCreateView, TaxUpdateView, TaxDeleteView,
    CompanyListView, CompanyCreateView, CompanyUpdateView, CompanyDeleteView,
    InvoiceListView, InvoiceCreateView, InvoiceSyncView,
    ReportView
)

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    path('taxes/', TaxListView.as_view(), name='tax_list'),
    path('taxes/create/', TaxCreateView.as_view(), name='tax_create'),
    path('taxes/<int:pk>/update/', TaxUpdateView.as_view(), name='tax_update'),
    path('taxes/<int:pk>/delete/', TaxDeleteView.as_view(), name='tax_delete'),
    
    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('companies/create/', CompanyCreateView.as_view(), name='company_create'),
    path('companies/<int:pk>/update/', CompanyUpdateView.as_view(), name='company_update'),
    path('companies/<int:pk>/delete/', CompanyDeleteView.as_view(), name='company_delete'),
    
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/create/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoices/sync/', InvoiceSyncView.as_view(), name='invoice_sync'),
    
    path('reports/', ReportView.as_view(), name='report'),
]