from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Customer, Estimate, Invoice, Item, OrderLine, Saler


class SalerViewsTestCase(TestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.user = self.UserModel.objects.create_user(
            email="user@test.com", password="password123"
        )
        self.admin = self.UserModel.objects.create_superuser(
            email="admin@test.com",
            password="strongpass123",
        )
        self.saler_0 = Saler.objects.create(
            name="computer corporation",
            adress="15 Maltings Farm",
            city="London",
            email="computerc@test.com",
            country="GB",
            phone_number="+590000001",
            postal_code="10001",
            logo="computercorp.png",
        )
        self.saler_1 = Saler.objects.create(
            name="riot",
            adress="44 Maltings Farm",
            city="London",
            email="riot@test.com",
            country="GB",
            postal_code="10001",
            phone_number="+590000004",
            logo="riot.png",
            is_active=False,
        )
        self.default_client = Client()
        self.default_client.login(
            username=self.user.email, password="password123"
        )
        self.admin_client = Client()
        self.admin_client.login(
            username=self.admin.email, password="strongpass123"
        )

    def test_list_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:saler_list"), follow=False
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user only see object when  is_active == True
        response_user = self.default_client.get(reverse("sales:saler_list"))
        self.assertEqual(response_user.status_code, 200)
        self.assertEqual(len(response_user.context["object_list"]), 1)
        self.assertContains(response_user, b"computer corporation")
        self.assertNotContains(response_user, b"riot")

        # Admin SHOULD see all object
        reponse_admin = self.admin_client.get(reverse("sales:saler_list"))
        self.assertEqual(reponse_admin.status_code, 200)
        self.assertEqual(len(reponse_admin.context["object_list"]), 2)
        self.assertContains(reponse_admin, b"computer corporation")
        self.assertContains(reponse_admin, b"riot")

    def test_create_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:saler_create"), follow=False
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user can see the create page
        response_user_get = self.default_client.get(
            reverse("sales:saler_create")
        )
        self.assertEqual(response_user_get.status_code, 200)
        self.assertContains(response_user_get, b"Add saler")

        # Authenticated user can create a saler
        new_saler_data = {
            "name": "msi",
            "adress": "44 Main Street",
            "city": "Bozeman",
            "email": "msi@test.com",
            "postal_code": "10001",
            "country": "US",
            "phone_number": "+12125552344",
        }
        salers = Saler.objects.all()
        self.assertEqual(len(salers), 2)
        response_user_post_0 = self.default_client.post(
            reverse("sales:saler_create"),
            new_saler_data,
            follow=True,
        )
        self.assertEqual(response_user_post_0.status_code, 200)
        messages = list(response_user_post_0.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f"{new_saler_data['name']} was created successfully",
        )
        salers = Saler.objects.all()
        self.assertEqual(len(salers), 3)
        self.assertRedirects(response_user_post_0, reverse("sales:saler_list"))
        self.assertContains(
            response_user_post_0, bytes(new_saler_data["name"], "utf8")
        )

    def test_update_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:saler_update", kwargs={"pk": self.saler_0.id}),
            follow=False,
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user can see the update page
        response_user_get = self.default_client.get(
            reverse("sales:saler_update", kwargs={"pk": self.saler_0.id})
        )
        self.assertEqual(response_user_get.status_code, 200)
        self.assertEqual(response_user_get.context["object"], self.saler_0)
        self.assertContains(response_user_get, b"Edit saler")

        # Authenticated user can update a saler instance
        updated_saler_data = {
            "name": "global IT",
            "adress": "15 Maltings Farm",
            "city": "London",
            "email": "globalit@test.com",
            "country": "GB",
            "phone_number": "+594694010203",
            "postal_code": "10001",
            "logo": "globalit.png",
        }
        response_user_post_0 = self.default_client.post(
            reverse("sales:saler_update", kwargs={"pk": self.saler_0.id}),
            updated_saler_data,
            follow=True,
        )
        self.assertEqual(response_user_post_0.status_code, 200)
        messages = list(response_user_post_0.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f"{updated_saler_data['name']} was updated successfully",
        )
        salers = Saler.objects.all()
        self.assertEqual(len(salers), 2)
        self.assertRedirects(response_user_post_0, reverse("sales:saler_list"))
        self.assertContains(
            response_user_post_0, bytes(updated_saler_data["name"], "utf8")
        )

    def test_delete_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:saler_delete", kwargs={"pk": self.saler_0.id}),
            follow=False,
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user can see the delete page
        response_user_get = self.default_client.get(
            reverse("sales:saler_delete", kwargs={"pk": self.saler_0.id})
        )
        self.assertEqual(response_user_get.status_code, 200)
        self.assertEqual(response_user_get.context["object"], self.saler_0)
        self.assertContains(response_user_get, b"Delete")

        # Authenticated user can << SOFT >> deletea saler instance
        response_user_post_0 = self.default_client.post(
            reverse("sales:saler_delete", kwargs={"pk": self.saler_0.id}),
            follow=True,
        )
        self.assertEqual(response_user_post_0.status_code, 200)
        messages = list(response_user_post_0.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Deleted successfully")
        salers = Saler.objects.all()
        self.assertEqual(len(salers), 2)
        self.assertRedirects(response_user_post_0, reverse("sales:saler_list"))
        self.assertContains(response_user_post_0, b"No saler yet.")
        deleted_saler = Saler.objects.get(pk=self.saler_0.id)
        self.assertFalse(deleted_saler.is_active)
        self.assertIsNotNone(deleted_saler.deleted_date)
        self.assertEqual(deleted_saler.deleted_by, self.user)


class CustomerViewsTestCase(TestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.user = self.UserModel.objects.create_user(
            email="user@test.com", password="password123"
        )
        self.admin = self.UserModel.objects.create_superuser(
            email="admin@test.com",
            password="strongpass123",
        )
        self.customer_0 = Customer.objects.create(
            name="Jhon Doe",
            adress="37 Maltings Farm",
            city="London",
            email="jhondoec@test.com",
            country="GB",
            phone_number="+590000001",
            postal_code="10001",
        )
        self.customer_1 = Customer.objects.create(
            name="Bob Carlos",
            adress="44 Maltings Farm",
            city="London",
            email="bobcarlos@test.com",
            country="GB",
            postal_code="10001",
            phone_number="+590000004",
            is_active=False,
        )
        self.default_client = Client()
        self.default_client.login(
            username=self.user.email, password="password123"
        )
        self.admin_client = Client()
        self.admin_client.login(
            username=self.admin.email, password="strongpass123"
        )

    def test_list_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:customer_list"), follow=False
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user only see object when  is_active == True
        response_user = self.default_client.get(reverse("sales:customer_list"))
        self.assertEqual(response_user.status_code, 200)
        self.assertEqual(len(response_user.context["object_list"]), 1)
        self.assertContains(response_user, b"Jhon Doe")
        self.assertNotContains(response_user, b"Bob Carlos")

        # Admin SHOULD see all object
        reponse_admin = self.admin_client.get(reverse("sales:customer_list"))
        self.assertEqual(reponse_admin.status_code, 200)
        self.assertEqual(len(reponse_admin.context["object_list"]), 2)
        self.assertContains(reponse_admin, b"Jhon Doe")
        self.assertContains(reponse_admin, b"Bob Carlos")

    def test_create_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:customer_create"), follow=False
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user can see the create page
        response_user_get = self.default_client.get(
            reverse("sales:customer_create")
        )
        self.assertEqual(response_user_get.status_code, 200)
        self.assertContains(response_user_get, b"Add customer")

        # Authenticated user can create a customer
        new_customer_data = {
            "name": "Zac Brand",
            "adress": "44 Main Street",
            "city": "Bozeman",
            "email": "zacbrand@test.com",
            "postal_code": "10002",
            "country": "US",
            "phone_number": "+12125552344",
        }
        customers = Customer.objects.all()
        self.assertEqual(len(customers), 2)
        response_user_post_0 = self.default_client.post(
            reverse("sales:customer_create"),
            new_customer_data,
            follow=True,
        )
        self.assertEqual(response_user_post_0.status_code, 200)
        messages = list(response_user_post_0.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f"{new_customer_data['name']} was created successfully",
        )
        customers = Customer.objects.all()
        self.assertEqual(len(customers), 3)
        self.assertRedirects(
            response_user_post_0, reverse("sales:customer_list")
        )
        self.assertContains(
            response_user_post_0, bytes(new_customer_data["name"], "utf8")
        )

    def test_update_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse(
                "sales:customer_update", kwargs={"pk": self.customer_0.id}
            ),
            follow=False,
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user can see the update page
        response_user_get = self.default_client.get(
            reverse("sales:customer_update", kwargs={"pk": self.customer_0.id})
        )
        self.assertEqual(response_user_get.status_code, 200)
        self.assertEqual(response_user_get.context["object"], self.customer_0)
        self.assertContains(response_user_get, b"Edit customer")

        # Authenticated user can update a customer instance
        updated_customer_data = {
            "name": "Lee Sin",
            "adress": "15 Maltings Farm",
            "city": "Atlanta",
            "email": "leesin@test.com",
            "country": "US",
            "phone_number": "+594694010203",
            "postal_code": "10003",
        }
        response_user_post_0 = self.default_client.post(
            reverse(
                "sales:customer_update", kwargs={"pk": self.customer_0.id}
            ),
            updated_customer_data,
            follow=True,
        )
        self.assertEqual(response_user_post_0.status_code, 200)
        messages = list(response_user_post_0.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f"{updated_customer_data['name']} was updated successfully",
        )
        customers = Customer.objects.all()
        self.assertEqual(len(customers), 2)
        self.assertRedirects(
            response_user_post_0, reverse("sales:customer_list")
        )
        self.assertContains(
            response_user_post_0, bytes(updated_customer_data["name"], "utf8")
        )

    def test_delete_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse(
                "sales:customer_delete", kwargs={"pk": self.customer_0.id}
            ),
            follow=False,
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user can see the delete page
        response_user_get = self.default_client.get(
            reverse("sales:customer_delete", kwargs={"pk": self.customer_0.id})
        )
        self.assertEqual(response_user_get.status_code, 200)
        self.assertEqual(response_user_get.context["object"], self.customer_0)
        self.assertContains(response_user_get, b"Delete")

        # Authenticated user can << SOFT >> deletea customer instance
        response_user_post_0 = self.default_client.post(
            reverse(
                "sales:customer_delete", kwargs={"pk": self.customer_0.id}
            ),
            follow=True,
        )
        self.assertEqual(response_user_post_0.status_code, 200)
        messages = list(response_user_post_0.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Deleted successfully")
        customers = Customer.objects.all()
        self.assertEqual(len(customers), 2)
        self.assertRedirects(
            response_user_post_0, reverse("sales:customer_list")
        )
        self.assertContains(response_user_post_0, b"No customer yet.")
        deleted_customer = Customer.objects.get(pk=self.customer_0.id)
        self.assertFalse(deleted_customer.is_active)
        self.assertIsNotNone(deleted_customer.deleted_date)
        self.assertEqual(deleted_customer.deleted_by, self.user)


class ItemViewsTestCase(TestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.user = self.UserModel.objects.create_user(
            email="user@test.com", password="password123"
        )
        self.admin = self.UserModel.objects.create_superuser(
            email="admin@test.com",
            password="strongpass123",
        )
        self.item_0 = Item.objects.create(
            label="Book : The Summer HouseThe Summer House",
            description="by James Patterson and Brendan DuBois",
            price_duty_free=12.55,
            tax=5.5,
        )
        self.item_1 = Item.objects.create(
            label="Book : Snap",
            description="by Belinda Bauer",
            price_duty_free=13.99,
            tax=7.5,
            is_active=False,
        )
        self.default_client = Client()
        self.default_client.login(
            username=self.user.email, password="password123"
        )
        self.admin_client = Client()
        self.admin_client.login(
            username=self.admin.email, password="strongpass123"
        )

    def test_list_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:item_list"), follow=False
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user only see object when  is_active == True
        response_user = self.default_client.get(reverse("sales:item_list"))
        self.assertEqual(response_user.status_code, 200)
        self.assertEqual(len(response_user.context["object_list"]), 1)
        self.assertContains(
            response_user, b"Book : The Summer HouseThe Summer House"
        )
        self.assertContains(response_user, b"12.55")
        self.assertContains(response_user, b"5.5")
        self.assertNotContains(response_user, b"Book : Snap")
        self.assertNotContains(response_user, b"13.99")
        self.assertNotContains(response_user, b"7.5")

        # Admin SHOULD see all object
        reponse_admin = self.admin_client.get(reverse("sales:item_list"))
        self.assertEqual(reponse_admin.status_code, 200)
        self.assertEqual(len(reponse_admin.context["object_list"]), 2)
        self.assertContains(
            reponse_admin, b"Book : The Summer HouseThe Summer House"
        )
        self.assertContains(reponse_admin, b"12.55")
        self.assertContains(reponse_admin, b"5.5")
        self.assertContains(reponse_admin, b"Book : Snap")
        self.assertContains(reponse_admin, b"13.99")
        self.assertContains(reponse_admin, b"7.5")

    def test_create_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:item_create"), follow=False
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user can see the create page
        response_user_get = self.default_client.get(
            reverse("sales:item_create")
        )
        self.assertEqual(response_user_get.status_code, 200)
        self.assertContains(response_user_get, b"Add item")

        # Authenticated user can create an item
        new_item_data = {
            "label": "Book : Scar Tissue",
            "description": "by  Anthony Kiedis",
            "price_duty_free": 50,
            "tax": 5,
        }
        items = Item.objects.all()
        self.assertEqual(len(items), 2)
        response_user_post_0 = self.default_client.post(
            reverse("sales:item_create"),
            new_item_data,
            follow=True,
        )
        self.assertEqual(response_user_post_0.status_code, 200)
        messages = list(response_user_post_0.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f"{new_item_data['label']} was created successfully",
        )
        items = Item.objects.all()
        self.assertEqual(len(items), 3)
        self.assertRedirects(response_user_post_0, reverse("sales:item_list"))
        self.assertContains(
            response_user_post_0, bytes(new_item_data["label"], "utf8")
        )

    def test_update_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:item_update", kwargs={"pk": self.item_0.id}),
            follow=False,
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user can see the update page
        response_user_get = self.default_client.get(
            reverse("sales:item_update", kwargs={"pk": self.item_0.id})
        )
        self.assertEqual(response_user_get.status_code, 200)
        self.assertEqual(response_user_get.context["object"], self.item_0)
        self.assertContains(response_user_get, b"Edit item")

        # Authenticated user can update an item instance
        updated_item_data = {
            "label": "Book : The Summer HouseThe Summer House",
            "description": "by James Patterson and Brendan DuBois",
            "price_duty_free": 150,
            "tax": 30,
        }
        response_user_post_0 = self.default_client.post(
            reverse("sales:item_update", kwargs={"pk": self.item_0.id}),
            updated_item_data,
            follow=True,
        )
        self.assertEqual(response_user_post_0.status_code, 200)
        messages = list(response_user_post_0.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f"{updated_item_data['label']} was updated successfully",
        )
        items = Item.objects.all()
        self.assertEqual(len(items), 2)
        self.assertRedirects(response_user_post_0, reverse("sales:item_list"))
        self.assertContains(
            response_user_post_0, bytes(updated_item_data["label"], "utf8")
        )

    def test_delete_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:item_delete", kwargs={"pk": self.item_0.id}),
            follow=False,
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user can see the delete page
        response_user_get = self.default_client.get(
            reverse("sales:item_delete", kwargs={"pk": self.item_0.id})
        )
        self.assertEqual(response_user_get.status_code, 200)
        self.assertEqual(response_user_get.context["object"], self.item_0)
        self.assertContains(response_user_get, b"Delete")

        # Authenticated user can << SOFT >> delete an item instance
        response_user_post_0 = self.default_client.post(
            reverse("sales:item_delete", kwargs={"pk": self.item_0.id}),
            follow=True,
        )
        self.assertEqual(response_user_post_0.status_code, 200)
        messages = list(response_user_post_0.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Deleted successfully")
        items = Item.objects.all()
        self.assertEqual(len(items), 2)
        self.assertRedirects(response_user_post_0, reverse("sales:item_list"))
        self.assertContains(response_user_post_0, b"No item yet.")
        deleted_item = Item.objects.get(pk=self.item_0.id)
        self.assertFalse(deleted_item.is_active)
        self.assertIsNotNone(deleted_item.deleted_date)
        self.assertEqual(deleted_item.deleted_by, self.user)


class EstimateViewsTestCase(TestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.user = self.UserModel.objects.create_user(
            email="user@test.com", password="password123"
        )
        self.admin = self.UserModel.objects.create_superuser(
            email="admin@test.com",
            password="strongpass123",
        )
        self.saler_0 = Saler.objects.create(
            name="computer corporation",
            adress="15 Maltings Farm",
            city="London",
            email="computerc@test.com",
            country="GB",
            phone_number="+590000001",
            postal_code="10001",
            logo="computercorp.png",
        )
        self.customer_0 = Customer.objects.create(
            name="Jhon Doe",
            adress="37 Maltings Farm",
            city="London",
            email="jhondoec@test.com",
            country="GB",
            phone_number="+590000001",
            postal_code="10001",
        )
        self.item_0 = Item.objects.create(
            label="Book : The Summer HouseThe Summer House",
            description="by James Patterson and Brendan DuBois",
            price_duty_free=100,
            tax=20,
        )
        self.item_1 = Item.objects.create(
            label="Book : Aftershocks",
            description="by Nadia Owusu",
            price_duty_free=200,
            tax=10,
        )
        self.order_line_0 = OrderLine.objects.create(
            item=self.item_0,
            quantity=2,
        )
        self.order_line_1 = OrderLine.objects.create(
            item=self.item_0,
            quantity=4,
        )
        self.estimate_0 = Estimate.objects.create(
            saler=self.saler_0,
            customer=self.customer_0,
            date=date.today(),
            validity_date=date.today(),
        )
        # add order line to the estimate
        self.estimate_0.order_lines.add(self.order_line_0)

        self.estimate_1 = Estimate.objects.create(
            saler=self.saler_0,
            customer=self.customer_0,
            date=date.today(),
            validity_date=date.today(),
            is_active=False,
        )
        # add order line to the estimate
        self.estimate_1.order_lines.add(self.order_line_1)

        self.default_client = Client()
        self.default_client.login(
            username=self.user.email, password="password123"
        )
        self.admin_client = Client()
        self.admin_client.login(
            username=self.admin.email, password="strongpass123"
        )

    def test_list_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:estimate_list"), follow=False
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user only see object when is_active == True
        response_user = self.default_client.get(reverse("sales:estimate_list"))
        self.assertEqual(response_user.status_code, 200)
        self.assertEqual(len(response_user.context["object_list"]), 1)
        self.assertContains(
            response_user, bytes(self.saler_0.name, "utf_8"), 1
        )
        self.assertContains(
            response_user, bytes(self.customer_0.name, "utf_8"), 1
        )
        self.assertContains(
            response_user, bytes(self.saler_0.name, "utf_8"), 1
        )
        self.assertContains(response_user, b"240")

        # Admin SHOULD see all object
        reponse_admin = self.admin_client.get(reverse("sales:estimate_list"))
        self.assertEqual(reponse_admin.status_code, 200)
        self.assertEqual(len(reponse_admin.context["object_list"]), 2)
        self.assertContains(
            reponse_admin, bytes(self.saler_0.name, "utf_8"), 2
        )
        self.assertContains(
            reponse_admin, bytes(self.customer_0.name, "utf_8"), 2
        )
        self.assertContains(reponse_admin, b"240")
        self.assertContains(reponse_admin, b"480")

    def test_detail_view(self):
        """Check if all users get corresponding response"""
        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse(
                "sales:estimate_detail", kwargs={"pk": self.estimate_0.id}
            ),
            follow=False,
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated can acces to instance when is_active == True
        response_user = self.default_client.get(
            reverse("sales:estimate_detail", kwargs={"pk": self.estimate_0.id})
        )
        self.assertEqual(response_user.status_code, 200)
        self.assertEqual(response_user.context["object"], self.estimate_0)
        self.assertContains(response_user, bytes(self.item_0.label, "utf_8"))
        self.assertContains(
            response_user,
            f"{float(self.estimate_0.total_price_duty_free):-2g}".encode(),
        )
        self.assertContains(
            response_user,
            f"{float(self.estimate_0.total_tax_price):-2g}".encode(),
        )
        self.assertContains(
            response_user,
            f"{float(self.estimate_0.total_price_including_tax):-2g}".encode(),
        )
        # Authenticated can acces to instance when is_active == False
        response_user_not_active = self.default_client.get(
            reverse("sales:estimate_detail", kwargs={"pk": self.estimate_1.id})
        )
        self.assertEqual(response_user_not_active.status_code, 404)

    def test_pdf_view(self):
        """Check if all users get corresponding response"""
        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:estimate_pdf", kwargs={"pk": self.estimate_0.id}),
            follow=False,
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated can acces to instance when is_active == True
        response_user = self.default_client.get(
            reverse("sales:estimate_pdf", kwargs={"pk": self.estimate_0.id})
        )
        self.assertEqual(response_user.status_code, 200)
        self.assertEqual(response_user["content-type"], "application/pdf")
        self.assertEqual(response_user.context["object"], self.estimate_0)

        # Authenticated can acces to instance when is_active == False
        response_user_not_active = self.default_client.get(
            reverse("sales:estimate_detail", kwargs={"pk": self.estimate_1.id})
        )
        self.assertEqual(response_user_not_active.status_code, 404)

    def test_create_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:estimate_create"), follow=False
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user can see the create page
        response_user_get = self.default_client.get(
            reverse("sales:estimate_create")
        )
        self.assertEqual(response_user_get.status_code, 200)
        self.assertContains(response_user_get, b"Add estimate")
        self.assertContains(response_user_get, b"Add more item")

        # Authenticated user can create a customer

        # get number of querry before create a new estimate
        number_of_query_before_create = len(Estimate.objects.all())

        # Update the previous order line and add a new oderline
        new_estimate_data = {
            "saler": self.saler_0.id,
            "customer": self.customer_0.id,
            "date": date.today(),
            "validity_date": date.today() + relativedelta(days=30),
            "form-TOTAL_FORMS": "1",
            "form-INITIAL_FORMS": "0",
            "form-MIN_NUM_FORMS	": "1",
            "form-0-item": self.item_0.id,
            "form-0-quantity": 8,
        }
        response_user_post_0 = self.default_client.post(
            reverse("sales:estimate_create"),
            new_estimate_data,
            follow=True,
        )

        self.assertEqual(response_user_post_0.status_code, 200)
        messages = list(response_user_post_0.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "The estimate was created successfully",
        )
        estimates = Estimate.objects.all()
        self.assertEqual(len(estimates), number_of_query_before_create + 1)
        self.assertRedirects(
            response_user_post_0, reverse("sales:estimate_list")
        )
        self.assertContains(
            response_user_post_0, bytes(self.saler_0.name, "utf_8"), 2
        )
        self.assertContains(
            response_user_post_0, bytes(self.customer_0.name, "utf_8"), 2
        )
        self.assertContains(response_user_post_0, b"240")
        self.assertContains(response_user_post_0, b"960")

    def test_update_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse(
                "sales:estimate_update", kwargs={"pk": self.estimate_0.id}
            ),
            follow=False,
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user can see the update page
        response_user_get = self.default_client.get(
            reverse("sales:estimate_update", kwargs={"pk": self.estimate_0.id})
        )
        self.assertEqual(response_user_get.status_code, 200)
        self.assertEqual(response_user_get.context["object"], self.estimate_0)
        self.assertContains(
            response_user_get,
            f"Edit {self.saler_0.name} estimate n° "
            f"{self.estimate_0.estimate_saler_number}",
        )

        # Authenticated user can update an estimate instance
        updated_estimate_data = {
            "saler": self.saler_0.id,
            "customer": self.customer_0.id,
            "date": date.today(),
            "validity_date": date.today() + relativedelta(days=30),
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "1",
            "form-MIN_NUM_FORMS	": "1",
            "form-0-id": self.order_line_0.id,
            "form-0-item": self.item_0.id,
            "form-0-quantity": 1,
            "form-1-id": "",
            "form-1-item": self.item_1.id,
            "form-1-quantity": 2,
        }
        response_user_post_0 = self.default_client.post(
            reverse(
                "sales:estimate_update", kwargs={"pk": self.estimate_0.id}
            ),
            updated_estimate_data,
            follow=True,
        )
        self.assertEqual(response_user_post_0.status_code, 200)
        messages = list(response_user_post_0.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "The estimate was updated successfully",
        )
        estimates = Estimate.objects.all()
        self.assertEqual(len(estimates), 2)
        self.assertRedirects(
            response_user_post_0, reverse("sales:estimate_list")
        )
        self.assertEqual(len(self.estimate_0.order_lines.all()), 2)
        self.assertContains(response_user_post_0, b"560")

    def test_delete_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse(
                "sales:estimate_delete", kwargs={"pk": self.estimate_0.id}
            ),
            follow=False,
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user can see the delete page
        response_user_get = self.default_client.get(
            reverse("sales:estimate_delete", kwargs={"pk": self.estimate_0.id})
        )
        self.assertEqual(response_user_get.status_code, 200)
        self.assertEqual(response_user_get.context["object"], self.estimate_0)
        self.assertContains(response_user_get, b"delete")

        # Authenticated user can << SOFT >> delete an estimate instance
        response_user_post_0 = self.default_client.post(
            reverse("sales:estimate_delete", kwargs={"pk": self.item_0.id}),
            follow=True,
        )
        self.assertEqual(response_user_post_0.status_code, 200)
        messages = list(response_user_post_0.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Deleted successfully")
        estimates = Estimate.objects.all()
        self.assertEqual(len(estimates), 2)
        self.assertRedirects(
            response_user_post_0, reverse("sales:estimate_list")
        )
        self.assertContains(response_user_post_0, b"No estimate yet.")
        deleted_estimate = Estimate.objects.get(pk=self.item_0.id)
        self.assertFalse(deleted_estimate.is_active)
        self.assertIsNotNone(deleted_estimate.deleted_date)
        self.assertEqual(deleted_estimate.deleted_by, self.user)


class InvoiceViewsTestCase(TestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.user = self.UserModel.objects.create_user(
            email="user@test.com", password="password123"
        )
        self.admin = self.UserModel.objects.create_superuser(
            email="admin@test.com",
            password="strongpass123",
        )
        self.saler_0 = Saler.objects.create(
            name="computer corporation",
            adress="15 Maltings Farm",
            city="London",
            email="computerc@test.com",
            country="GB",
            phone_number="+590000001",
            postal_code="10001",
            logo="computercorp.png",
        )
        self.customer_0 = Customer.objects.create(
            name="Jhon Doe",
            adress="37 Maltings Farm",
            city="London",
            email="jhondoec@test.com",
            country="GB",
            phone_number="+590000001",
            postal_code="10001",
        )
        self.item_0 = Item.objects.create(
            label="Book : The Summer HouseThe Summer House",
            description="by James Patterson and Brendan DuBois",
            price_duty_free=100,
            tax=20,
        )
        self.item_1 = Item.objects.create(
            label="Book : Aftershocks",
            description="by Nadia Owusu",
            price_duty_free=200,
            tax=10,
        )
        self.order_line_0 = OrderLine.objects.create(
            item=self.item_0,
            quantity=2,
        )
        self.order_line_1 = OrderLine.objects.create(
            item=self.item_0,
            quantity=4,
        )
        self.invoice_0 = Invoice.objects.create(
            saler=self.saler_0,
            customer=self.customer_0,
            date=date.today(),
            is_paid=False,
        )
        # add order line to the invoice
        self.invoice_0.order_lines.add(self.order_line_0)

        self.invoice_1 = Invoice.objects.create(
            saler=self.saler_0,
            customer=self.customer_0,
            date=date.today(),
            is_paid=True,
            is_active=False,
        )
        # add order line to the invoice
        self.invoice_1.order_lines.add(self.order_line_1)

        self.default_client = Client()
        self.default_client.login(
            username=self.user.email, password="password123"
        )
        self.admin_client = Client()
        self.admin_client.login(
            username=self.admin.email, password="strongpass123"
        )

    def test_list_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:invoice_list"), follow=False
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user only see object when is_active == True
        response_user = self.default_client.get(reverse("sales:invoice_list"))
        self.assertEqual(response_user.status_code, 200)
        self.assertEqual(len(response_user.context["object_list"]), 1)
        self.assertContains(
            response_user, bytes(self.saler_0.name, "utf_8"), 1
        )
        self.assertContains(
            response_user, bytes(self.customer_0.name, "utf_8"), 1
        )
        self.assertContains(
            response_user, bytes(self.saler_0.name, "utf_8"), 1
        )
        self.assertContains(response_user, b"240")

        # Admin SHOULD see all object
        reponse_admin = self.admin_client.get(reverse("sales:invoice_list"))
        self.assertEqual(reponse_admin.status_code, 200)
        self.assertEqual(len(reponse_admin.context["object_list"]), 2)
        self.assertContains(
            reponse_admin, bytes(self.saler_0.name, "utf_8"), 2
        )
        self.assertContains(
            reponse_admin, bytes(self.customer_0.name, "utf_8"), 2
        )
        self.assertContains(reponse_admin, b"240")
        self.assertContains(reponse_admin, b"480")

    def test_detail_view(self):
        """Check if all users get corresponding response"""
        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:invoice_detail", kwargs={"pk": self.invoice_0.id}),
            follow=False,
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated can acces to instance when is_active == True
        response_user = self.default_client.get(
            reverse("sales:invoice_detail", kwargs={"pk": self.invoice_0.id})
        )
        self.assertEqual(response_user.status_code, 200)
        self.assertEqual(response_user.context["object"], self.invoice_0)
        self.assertContains(response_user, bytes(self.item_0.label, "utf_8"))
        self.assertContains(
            response_user,
            f"{float(self.invoice_0.total_price_duty_free):-2g}".encode(),
        )
        self.assertContains(
            response_user,
            f"{float(self.invoice_0.total_tax_price):-2g}".encode(),
        )
        self.assertContains(
            response_user,
            f"{float(self.invoice_0.total_price_including_tax):-2g}".encode(),
        )
        # Authenticated can acces to instance when is_active == False
        response_user_not_active = self.default_client.get(
            reverse("sales:invoice_detail", kwargs={"pk": self.invoice_1.id})
        )
        self.assertEqual(response_user_not_active.status_code, 404)

    def test_pdf_view(self):
        """Check if all users get corresponding response"""
        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:invoice_pdf", kwargs={"pk": self.invoice_0.id}),
            follow=False,
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated can acces to instance when is_active == True
        response_user = self.default_client.get(
            reverse("sales:invoice_pdf", kwargs={"pk": self.invoice_0.id})
        )
        self.assertEqual(response_user.status_code, 200)
        self.assertEqual(response_user["content-type"], "application/pdf")
        self.assertEqual(response_user.context["object"], self.invoice_0)

        # Authenticated can acces to instance when is_active == False
        response_user_not_active = self.default_client.get(
            reverse("sales:invoice_detail", kwargs={"pk": self.invoice_1.id})
        )
        self.assertEqual(response_user_not_active.status_code, 404)

    def test_create_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:invoice_create"), follow=False
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user can see the create page
        response_user_get = self.default_client.get(
            reverse("sales:invoice_create")
        )
        self.assertEqual(response_user_get.status_code, 200)
        self.assertContains(response_user_get, b"Add invoice")
        self.assertContains(response_user_get, b"Add more item")

        # Authenticated user can create a customer

        # get number of querry before create a new invoice
        number_of_query_before_create = len(Invoice.objects.all())

        new_invoice_data = {
            "saler": self.saler_0.id,
            "customer": self.customer_0.id,
            "date": date.today(),
            "is_paid": True,
            "form-TOTAL_FORMS": "1",
            "form-INITIAL_FORMS": "0",
            "form-MIN_NUM_FORMS	": "1",
            "form-0-item": self.item_0.id,
            "form-0-quantity": 8,
        }
        response_user_post_0 = self.default_client.post(
            reverse("sales:invoice_create"),
            new_invoice_data,
            follow=True,
        )

        self.assertEqual(response_user_post_0.status_code, 200)
        messages = list(response_user_post_0.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "The invoice was created successfully",
        )
        invoices = Invoice.objects.all()
        self.assertEqual(len(invoices), number_of_query_before_create + 1)
        self.assertRedirects(
            response_user_post_0, reverse("sales:invoice_list")
        )
        self.assertContains(
            response_user_post_0, bytes(self.saler_0.name, "utf_8"), 2
        )
        self.assertContains(
            response_user_post_0, bytes(self.customer_0.name, "utf_8"), 2
        )
        self.assertContains(response_user_post_0, b"240")
        self.assertContains(response_user_post_0, b"960")

    def test_update_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:invoice_update", kwargs={"pk": self.invoice_0.id}),
            follow=False,
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)
        self.assertFalse(self.invoice_0.is_paid, False)

        # Authenticated user can see the update page
        response_user_get = self.default_client.get(
            reverse("sales:invoice_update", kwargs={"pk": self.invoice_0.id})
        )
        self.assertEqual(response_user_get.status_code, 200)
        self.assertEqual(response_user_get.context["object"], self.invoice_0)
        self.assertContains(
            response_user_get,
            f"Edit {self.saler_0.name} invoice n° "
            f"{self.invoice_0.invoice_saler_number}",
        )

        # Authenticated user can update an invoice instance
        # Update the previous order line and add a new oder line
        updated_invoice_data = {
            "saler": self.saler_0.id,
            "customer": self.customer_0.id,
            "date": date.today(),
            "is_paid": True,
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "1",
            "form-MIN_NUM_FORMS	": "1",
            "form-0-id": self.order_line_0.id,
            "form-0-item": self.item_0.id,
            "form-0-quantity": 1,
            "form-1-id": "",
            "form-1-item": self.item_1.id,
            "form-1-quantity": 2,
        }
        response_user_post_0 = self.default_client.post(
            reverse("sales:invoice_update", kwargs={"pk": self.invoice_0.id}),
            updated_invoice_data,
            follow=True,
        )
        self.assertEqual(response_user_post_0.status_code, 200)
        messages = list(response_user_post_0.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "The invoice was updated successfully",
        )
        updated_instance = Invoice.objects.get(pk=self.invoice_0.id)
        self.assertTrue(updated_instance.is_paid)
        invoices = Invoice.objects.all()
        self.assertEqual(len(invoices), 2)
        self.assertRedirects(
            response_user_post_0, reverse("sales:invoice_list")
        )
        self.assertEqual(len(self.invoice_0.order_lines.all()), 2)
        self.assertContains(response_user_post_0, b"560")

    def test_delete_view(self):
        """Check if all users get corresponding response"""

        # Anonymous user get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:invoice_delete", kwargs={"pk": self.invoice_0.id}),
            follow=False,
        )
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertIn(reverse("users:login"), response_anonymous.url)

        # Authenticated user can see the delete page
        response_user_get = self.default_client.get(
            reverse("sales:invoice_delete", kwargs={"pk": self.invoice_0.id})
        )
        self.assertEqual(response_user_get.status_code, 200)
        self.assertEqual(response_user_get.context["object"], self.invoice_0)
        self.assertContains(response_user_get, b"delete")

        # Authenticated user can << SOFT >> delete an invoice instance
        response_user_post_0 = self.default_client.post(
            reverse("sales:invoice_delete", kwargs={"pk": self.item_0.id}),
            follow=True,
        )
        self.assertEqual(response_user_post_0.status_code, 200)
        messages = list(response_user_post_0.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Deleted successfully")
        invoices = Invoice.objects.all()
        self.assertEqual(len(invoices), 2)
        self.assertRedirects(
            response_user_post_0, reverse("sales:invoice_list")
        )
        self.assertContains(response_user_post_0, b"No invoice yet.")
        deleted_invoice = Invoice.objects.get(pk=self.item_0.id)
        self.assertFalse(deleted_invoice.is_active)
        self.assertIsNotNone(deleted_invoice.deleted_date)
        self.assertEqual(deleted_invoice.deleted_by, self.user)
