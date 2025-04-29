from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Company, Client, Product, Tax, Invoice, InvoiceItem
from django.utils import timezone
import random
from decimal import Decimal
import datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Generates sample data for the invoicing system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating sample data...')
        
        # Create admin user if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        
        # Create companies
        companies = []
        company_names = ['TechSolutions SAS', 'Comercial El Éxito', 'Cafetería Colombiana', 'Artesanías del Valle']
        
        for name in company_names:
            if not Company.objects.filter(business_name=name).exists():
                company = Company.objects.create(
                    business_name=name,
                    nit=f'9{random.randint(10000000, 99999999)}',
                    tax_regime='common',
                    address=f'Calle {random.randint(1, 100)} #{random.randint(1, 100)}-{random.randint(1, 100)}',
                    phone=f'+57 {random.randint(300, 350)} {random.randint(1000000, 9999999)}',
                    email=f'info@{name.lower().replace(" ", "")}.com.co'
                )
                companies.append(company)
                self.stdout.write(f'Created company: {name}')
        
        if not companies:
            companies = list(Company.objects.all())
            if not companies:
                self.stdout.write(self.style.WARNING('No companies found or created'))
                return
        
        # Create taxes
        taxes = []
        tax_data = [
            {'tax_type': 'IVA', 'rate': Decimal('19.00'), 'description': 'Impuesto al Valor Agregado 19%'},
            {'tax_type': 'IVA', 'rate': Decimal('5.00'), 'description': 'Impuesto al Valor Agregado 5%'},
            {'tax_type': 'IVA', 'rate': Decimal('0.00'), 'description': 'Impuesto al Valor Agregado 0%'},
            {'tax_type': 'INC', 'rate': Decimal('8.00'), 'description': 'Impuesto Nacional al Consumo 8%'}
        ]
        
        for tax_item in tax_data:
            if not Tax.objects.filter(tax_type=tax_item['tax_type'], rate=tax_item['rate']).exists():
                tax = Tax.objects.create(
                    tax_type=tax_item['tax_type'],
                    rate=tax_item['rate'],
                    description=tax_item['description']
                )
                taxes.append(tax)
                self.stdout.write(f'Created tax: {tax_item["tax_type"]} ({tax_item["rate"]}%)')
        
        if not taxes:
            taxes = list(Tax.objects.all())
            if not taxes:
                self.stdout.write(self.style.WARNING('No taxes found or created'))
                return
        
        # Create clients
        clients = []
        client_names = [
            'Juan Pérez', 'María López', 'Empresas XYZ', 'Distribuidora Nacional',
            'Carlos Ramírez', 'Ana Gómez', 'Inversiones ABC', 'Restaurante El Sabor'
        ]
        
        for i, name in enumerate(client_names):
            company = companies[i % len(companies)]  # Distribute clients among companies
            if not Client.objects.filter(name=name, company=company).exists():
                client = Client.objects.create(
                    company=company,
                    identification_type='CC' if i < 4 else 'NIT',
                    identification_number=f'{random.randint(10000000, 99999999)}',
                    name=name,
                    address=f'Carrera {random.randint(1, 100)} #{random.randint(1, 100)}-{random.randint(1, 100)}',
                    phone=f'+57 {random.randint(300, 350)} {random.randint(1000000, 9999999)}',
                    email=f'{name.lower().replace(" ", ".")}@example.com'
                )
                clients.append(client)
                self.stdout.write(f'Created client: {name}')
        
        if not clients:
            clients = list(Client.objects.all())
            if not clients:
                self.stdout.write(self.style.WARNING('No clients found or created'))
                return
        
        # Create products
        products = []
        product_data = [
            {'description': 'Laptop Dell XPS', 'price': Decimal('3500000.00')},
            {'description': 'Smartphone Samsung', 'price': Decimal('1200000.00')},
            {'description': 'Impresora HP', 'price': Decimal('850000.00')},
            {'description': 'Monitor LG 24"', 'price': Decimal('650000.00')},
            {'description': 'Teclado Mecánico', 'price': Decimal('280000.00')},
            {'description': 'Mouse Inalámbrico', 'price': Decimal('120000.00')},
            {'description': 'Audífonos Bluetooth', 'price': Decimal('180000.00')},
            {'description': 'Cámara Web HD', 'price': Decimal('230000.00')},
            {'description': 'Disco Duro Externo 1TB', 'price': Decimal('320000.00')},
            {'description': 'Memoria USB 64GB', 'price': Decimal('75000.00')}
        ]
        
        for i, product_item in enumerate(product_data):
            company = companies[i % len(companies)]  # Distribute products among companies
            if not Product.objects.filter(description=product_item['description'], company=company).exists():
                tax = random.choice(taxes)
                product = Product.objects.create(
                    company=company,
                    code=f'PROD-{i+1:03d}',
                    description=product_item['description'],
                    price=product_item['price'],
                    tax=tax,
                    category='Tecnología',
                    stock_quantity=random.randint(5, 50)
                )
                products.append(product)
                self.stdout.write(f'Created product: {product_item["description"]}')
        
        if not products:
            products = list(Product.objects.all())
            if not products:
                self.stdout.write(self.style.WARNING('No products found or created'))
                return
        
        # Create invoices with items
        invoice_statuses = ['draft', 'pending', 'validated', 'rejected']
        current_year = timezone.now().year
        
        for i in range(1, 21):  # Create 20 invoices
            invoice_number = f'FACT-{current_year}-{i:04d}'
            
            if not Invoice.objects.filter(invoice_number=invoice_number).exists():
                company = random.choice(companies)
                client = random.choice([c for c in clients if c.company == company])  # Client from same company
                status = random.choice(invoice_statuses)
                
                # Create invoice with a date in 2025 (for reporting purposes)
                issue_date = datetime.date(2025, random.randint(1, 4), random.randint(1, 28))
                
                invoice = Invoice.objects.create(
                    company=company,
                    client=client,
                    invoice_number=invoice_number,
                    issue_date=issue_date,
                    status=status,
                    total_amount=Decimal('0.00'),  # Will be updated after adding items
                    tax_amount=Decimal('0.00'),    # Will be updated after adding items
                    discount_amount=Decimal('0.00')
                )
                
                # Add 1-5 random products to the invoice
                total_amount = Decimal('0.00')
                tax_amount = Decimal('0.00')
                
                company_products = [p for p in products if p.company == company]
                if not company_products:
                    company_products = products  # Fallback to all products
                
                for _ in range(random.randint(1, 5)):
                    product = random.choice(company_products)
                    quantity = random.randint(1, 5)
                    unit_price = product.price
                    
                    # Calculate tax amount for this item
                    item_tax_amount = (unit_price * quantity) * (product.tax.rate / Decimal('100.00'))
                    item_subtotal = (unit_price * quantity) + item_tax_amount
                    
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        product=product,
                        quantity=quantity,
                        unit_price=unit_price,
                        tax_amount=item_tax_amount,
                        subtotal=item_subtotal
                    )
                    
                    total_amount += item_subtotal
                    tax_amount += item_tax_amount
                
                # Update invoice totals
                invoice.total_amount = total_amount
                invoice.tax_amount = tax_amount
                invoice.save()
                
                # Add CUFE for validated invoices
                if status == 'validated':
                    invoice.cufe = f'cufe-{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}'
                    invoice.digital_signature = 'mock_signature_data'
                    invoice.save()
                
                self.stdout.write(f'Created invoice: {invoice_number}')
        
        self.stdout.write(self.style.SUCCESS('Sample data generation completed!'))