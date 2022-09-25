from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Saler, Customer, Item, OrderLine, Estimate, Invoice
from unittest import mock
from datetime import datetime, timezone, date
from dateutil.relativedelta import relativedelta


class SalerTests(TestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.admin_user = UserModel.objects.create_superuser(
            email="superuser@test.com", password="strongsecret123"
        )

    def test_create_saler(self):
        """Create a saler instance and check the properties data"""
        saler_data = {
            "name": "Tesla",
            "adress": "15 Town Orchards",
            "city": "Atlanta",
            "email": "tesla@test.com",
            "country": "US",
            "phone_number": "+594000000",
            "logo": "teslalogo.png",
            "user": self.admin_user,
        }
        # set the datime for testing the created_date
        mocked_datetime = datetime.now(timezone.utc)
        with mock.patch(
            "django.utils.timezone.now",
            mock.Mock(return_value=mocked_datetime),
        ):
            saler = Saler.objects.create(
                name=saler_data["name"],
                adress=saler_data["adress"],
                city=saler_data["city"],
                email=saler_data["email"],
                country=saler_data["country"],
                phone_number=saler_data["phone_number"],
                logo=saler_data["logo"],
                created_by=saler_data["user"],
            )
        self.assertEqual(saler.name, saler_data["name"])
        self.assertEqual(saler.adress, saler_data["adress"])
        self.assertEqual(saler.city, saler_data["city"])
        self.assertEqual(saler.email, saler_data["email"])
        self.assertEqual(saler.country, saler_data["country"])
        self.assertEqual(saler.phone_number, saler_data["phone_number"])
        self.assertEqual(saler.logo, saler_data["logo"])
        self.assertTrue(saler.is_active)
        self.assertEqual(saler.created_by, saler_data["user"])
        self.assertEqual(saler.created_date, mocked_datetime)
        self.assertEqual(saler.modified_date, mocked_datetime)
        self.assertIsNone(saler.modified_by)
        self.assertIsNone(saler.deleted_date)
        self.assertIsNone(saler.deleted_by)
        self.assertEqual(str(saler), saler_data["name"])


class CustomerTests(TestCase):
    def test_create_customer(self):
        """Create a customer instance and check the properties data"""
        customer_data = {
            "name": "Jhone Doe",
            "adress": "44 Morrison Royd",
            "city": "Atlanta",
            "email": "jhondoe@test.com",
            "country": "US",
            "phone_number": "+594000201",
        }

        customer = Customer.objects.create(
            name=customer_data["name"],
            adress=customer_data["adress"],
            city=customer_data["city"],
            email=customer_data["email"],
            country=customer_data["country"],
            phone_number=customer_data["phone_number"],
        )
        self.assertEqual(customer.name, customer_data["name"])
        self.assertEqual(customer.adress, customer_data["adress"])
        self.assertEqual(customer.city, customer_data["city"])
        self.assertEqual(customer.email, customer_data["email"])
        self.assertEqual(customer.country, customer_data["country"])
        self.assertEqual(customer.phone_number, customer_data["phone_number"])
        self.assertEqual(str(customer), customer_data["name"])


class ItemTests(TestCase):
    def test_create_item(self):
        """Create an item instance and check the properties data"""
        item_data = {
            "label": "Verity",
            "description": "Paper book written by Colleen Hoover",
            "price_duty_free": 100,
            "tax": 20,
        }
        tax_price = item_data["price_duty_free"] * (item_data["tax"] / 100)
        including_tax = item_data["price_duty_free"] + tax_price
        item = Item.objects.create(
            label=item_data["label"],
            description=item_data["description"],
            price_duty_free=item_data["price_duty_free"],
            tax=item_data["tax"],
        )

        self.assertEqual(item.label, item_data["label"])
        self.assertEqual(item.description, item_data["description"])
        self.assertEqual(item.price_duty_free, item_data["price_duty_free"])
        self.assertEqual(item.tax, item_data["tax"])
        self.assertEqual(item.tax_price, tax_price)
        self.assertEqual(item.including_tax, including_tax)
        self.assertEqual(str(item), item_data["label"])


class OrderLineTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            label="HP Laptop 15s-fq2007sf",
            description="PC Portable 15.6' FHD (AMZ Ryzen 5, RAM 8 Go, SSD 256 Go)",
            price_duty_free=1000,
            tax=15,
        )

    def test_create_orderline(self):
        """Create an odder_line instance and check the properties data"""
        order_line_data = {
            "item": self.item,
            "quantity": 4,
        }
        order_line = OrderLine.objects.create(
            item=order_line_data["item"], quantity=order_line_data["quantity"]
        )
        subtotal_duty_free = (
            order_line_data["item"].price_duty_free
            * order_line_data["quantity"]
        )
        subtotal_tax_price = (
            order_line_data["item"].tax_price * order_line_data["quantity"]
        )
        subtotal_including_tax = (
            order_line_data["item"].including_tax * order_line_data["quantity"]
        )

        self.assertEqual(order_line.item, order_line_data["item"])
        self.assertEqual(order_line.quantity, order_line_data["quantity"])
        self.assertEqual(order_line.subtotal_duty_free, subtotal_duty_free)
        self.assertEqual(order_line.subtotal_tax_price, subtotal_tax_price)
        self.assertEqual(
            order_line.subtotal_including_tax, subtotal_including_tax
        )
        self.assertEqual(
            str(order_line),
            f"{order_line_data['item'].label} - {order_line_data['quantity']}",
        )


class EstimateTest(TestCase):
    def setUp(self):
        self.saler = Saler.objects.create(
            name="computer corporation",
            adress="15 Maltings Farm",
            city="London",
            email="computerc@test.com",
            country="UK",
            phone_number="+590000001",
            logo="computercorp.png",
        )
        self.customer = Customer.objects.create(
            name="Lee sin",
            adress="44 Park Street",
            city="London",
            email="leesinc@test.com",
            country="UK",
            phone_number="+590000002",
        )
        self.item_0 = Item.objects.create(
            label="MSI titan gt77",
            description="PC Portable 17' FHD (Intel Core i9, RAM 32 Go, SSD 2 To)",
            price_duty_free=4000,
            tax=5,
        )
        self.item_1 = Item.objects.create(
            label="Microsoft Surface Book",
            description="PC Portable 15' FHD (Intel Core i7, RAM 32 Go, SSD 512 Go)",
            price_duty_free=3800,
            tax=15,
        )
        self.order_line_0 = OrderLine.objects.create(
            item=self.item_0,
            quantity=5,
        )
        self.order_line_1 = OrderLine.objects.create(
            item=self.item_1,
            quantity=5,
        )

    def test_create_estimate(self):
        """Create an estimate instance and check the properties data and methods"""
        default_date = date.today() + relativedelta(days=30)
        estimate_data = {
            "saler": self.saler,
            "customer": self.customer,
            "order_lines": [self.order_line_0, self.order_line_1],
            "date": date.today(),
            "validity_date": default_date,
        }
        estimate = Estimate.objects.create(
            saler=estimate_data["saler"],
            customer=estimate_data["customer"],
            date=estimate_data["date"],
            validity_date=estimate_data["validity_date"],
        )
        total_price_duty_free = 0
        total_price_including_tax = 0
        total_tax_price = 0
        # add item to the order line to the estimate
        estimate.order_lines.set(estimate_data["order_lines"])
        for order_line in estimate_data["order_lines"]:
            # calculate the total of the estimate
            total_price_duty_free += order_line.subtotal_duty_free
            total_tax_price += order_line.subtotal_including_tax
            total_price_including_tax += order_line.subtotal_including_tax

        self.assertEqual(estimate.saler, estimate_data["saler"])
        self.assertEqual(estimate.customer, estimate_data["customer"])
        self.assertEqual(estimate.date, estimate_data["date"])
        self.assertEqual(
            estimate.validity_date, estimate_data["validity_date"]
        )
        for order_line in estimate_data["order_lines"]:
            self.assertIn(order_line, estimate.order_lines.all())
        self.assertEqual(estimate.total_price_duty_free, total_price_duty_free)
        self.assertEqual(estimate.total_tax_price, total_tax_price)
        self.assertEqual(
            estimate.total_price_including_tax, total_price_including_tax
        )
        self.assertEqual(
            str(estimate),
            f"{estimate_data['saler']} - {estimate_data['customer']} - {estimate_data['date']}",
        )
        # check len number of invoice
        before_invoices = Invoice.objects.all()
        self.assertEqual(len(before_invoices), 0)
        self.assertTrue(estimate.turn_into_an_invoice())
        after_invoices = Invoice.objects.all()
        self.assertEqual(len(after_invoices), 1)
        invoice = Invoice.objects.all().first()
        self.assertEqual(invoice.saler, estimate.saler)
        self.assertEqual(invoice.customer, estimate.customer)
        self.assertEqual(invoice.customer, estimate.customer)
        self.assertEqual(
            len(invoice.order_lines.all()), len(estimate.order_lines.all())
        )
        self.assertFalse(invoice.is_paid)


class InvoiceTest(TestCase):
    def setUp(self):
        self.saler = Saler.objects.create(
            name="BookShop",
            adress="25 Linking park Street",
            city="London",
            email="bookshop@test.com",
            country="UK",
            phone_number="+590000004",
            logo="bookshop.png",
        )
        self.customer = Customer.objects.create(
            name="Brand Zac",
            adress="44 Roberto Street",
            city="London",
            email="brandzacc@test.com",
            country="UK",
            phone_number="+590000504",
        )
        self.item_0 = Item.objects.create(
            label="Don Quixote",
            description="Author : Miguel de Cervantes",
            price_duty_free=40,
            tax=2.5,
        )
        self.item_1 = Item.objects.create(
            label="Ulysse",
            description="Author : James Joyce",
            price_duty_free=25,
            tax=2.5,
        )
        self.order_line_0 = OrderLine.objects.create(
            item=self.item_0,
            quantity=30,
        )
        self.order_line_1 = OrderLine.objects.create(
            item=self.item_1,
            quantity=20,
        )

    def test_create_invoice(self):
        """Create an invoice instance and check the properties data"""
        invoice_data = {
            "saler": self.saler,
            "customer": self.customer,
            "order_lines": [self.order_line_0, self.order_line_1],
            "date": date.today(),
            "is_paid": True,
        }
        invoice = Invoice.objects.create(
            saler=invoice_data["saler"],
            customer=invoice_data["customer"],
            date=invoice_data["date"],
            is_paid=invoice_data["is_paid"],
        )
        total_price_duty_free = 0
        total_price_including_tax = 0
        total_tax_price = 0
        # add item to the order line to the estimate
        invoice.order_lines.set(invoice_data["order_lines"])
        for order_line in invoice_data["order_lines"]:
            # calculate the total of the invoice
            total_price_duty_free += order_line.subtotal_duty_free
            total_tax_price += order_line.subtotal_including_tax
            total_price_including_tax += order_line.subtotal_including_tax

        self.assertEqual(invoice.saler, invoice_data["saler"])
        self.assertEqual(invoice.customer, invoice_data["customer"])
        self.assertEqual(invoice.date, invoice_data["date"])
        self.assertTrue(invoice.is_paid)
        for order_line in invoice_data["order_lines"]:
            self.assertIn(order_line, invoice.order_lines.all())
        self.assertEqual(invoice.total_price_duty_free, total_price_duty_free)
        self.assertEqual(invoice.total_tax_price, total_tax_price)
        self.assertEqual(
            invoice.total_price_including_tax, total_price_including_tax
        )
        self.assertEqual(
            str(invoice),
            f"{invoice_data['saler']} - {invoice_data['customer']} - {invoice_data['date']}",
        )
