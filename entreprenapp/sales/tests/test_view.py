from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Saler


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
            country="US",
            phone_number="+590000001",
            postal_code="10001",
            logo="computercorp.png",
        )
        self.saler_1 = Saler.objects.create(
            name="riot",
            adress="44 Maltings Farm",
            city="London",
            email="riot@test.com",
            country="US",
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

        # Anonymous get redirect to the login
        response_anonymous = self.client.get(
            reverse("sales:saler_create"), follow=False
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

        # Anonymous get redirect to the login
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

        # Anonymous get redirect to the login
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
            "country": "US",
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

        # Anonymous get redirect to the login
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
