from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class UsersManagersTests(TestCase):
    def setUp(self):
        self.UserModel = get_user_model()

    def test_create_user(self):
        user_data = {
            "email": "jhondoe@test.com",
            "password": "abigpassword123",
        }

        user = self.UserModel.objects.create_user(
            email=user_data["email"], password=user_data["password"]
        )
        self.assertEqual(user.email, user_data["email"])
        self.assertNotEqual(user.password, user_data["password"])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(str(user), user_data["email"])
        try:
            # Username is None for the AbstractUser option
            # Username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            # Try create an user without email and password
            self.UserModel.objects.create_user()
        with self.assertRaises(TypeError):
            # Try create an user with empty email and without password
            self.UserModel.objects.create_user(email="")
        with self.assertRaises(ValueError):
            # Try create an user with empty email and a good password
            self.UserModel.objects.create_user(email="", password="foo")

    def test_create_superuser(self):

        admin_user_data = {
            "email": "superuser@test.com",
            "password": "asuperpassword1234",
        }
        admin_user = self.UserModel.objects.create_superuser(
            email=admin_user_data["email"],
            password=admin_user_data["password"],
        )
        self.assertEqual(admin_user.email, admin_user_data["email"])
        self.assertNotEqual(admin_user.password, admin_user_data["password"])
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(str(admin_user), admin_user_data["email"])
        try:
            # Username is None for the AbstractUser option
            # Username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            # Try to create a super user with is_superuser set to False
            self.UserModel.objects.create_superuser(
                email="superuser2@test.com",
                password="megapasswordforadmin123",
                is_superuser=False,
            )
        with self.assertRaises(ValueError):
            # Try to create a super user with is_staff set to False
            self.UserModel.objects.create_superuser(
                email="superuser2@test.com",
                password="megapasswordforadmin123",
                is_staff=False,
            )


class UsersViewTests(TestCase):
    def setUp(self):
        self.UserModel = get_user_model()

        self.admin_user_data = {
            "email": "superuser@test.com",
            "password": "asuperpassword1234",
        }
        self.UserModel.objects.create_superuser(**self.admin_user_data)

    def test_reset_password(self):
        response_get = self.client.get(
            reverse("users:password_reset"), follow=False
        )
        self.assertEqual(response_get.status_code, 200)
        self.assertContains(response_get, b"password")

        response_post_0 = self.client.post(
            reverse("users:password_reset"),
            {"email": self.admin_user_data["email"]},
            follow=True,
        )
        self.assertEqual(response_post_0.status_code, 200)
        self.assertContains(response_post_0, b"Check the next step")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], self.admin_user_data["email"])
        self.assertEqual(
            mail.outbox[0].subject, "Password reset on testserver"
        )
        self.assertIn("http://testserver/accounts/", mail.outbox[0].body)

    def test_password_reset_confirm_valid_token(self):
        # With a valid token user can acces to the get page
        user = self.UserModel.objects.get(email="superuser@test.com")
        token = default_token_generator.make_token(user)
        uid_user = (urlsafe_base64_encode(force_bytes(user.pk)),)
        response_get_valid_token = self.client.get(
            reverse(
                "users:password_reset_confirm",
                kwargs={"uidb64": uid_user, "token": token},
            ),
            follow=True,
        )
        self.assertEqual(response_get_valid_token.status_code, 200)
        self.assertContains(response_get_valid_token, b"Change your password")

        # Change the new password
        new_password = {
            "new_password1": "anewstrongpassword85:!",
            "new_password2": "anewstrongpassword85:!",
        }

        response_post_valid_token = self.client.post(
            reverse(
                "users:password_reset_confirm",
                kwargs={"uidb64": uid_user, "token": "set-password"},
            ),
            new_password,
            follow=True,
        )
        self.assertEqual(response_post_valid_token.status_code, 200)
        self.assertContains(response_post_valid_token, b"Well done")
        self.assertContains(
            response_post_valid_token, b"Your password has been set."
        )
        login_url = reverse("users:login")
        # Check if the login url is on the page
        self.assertContains(
            response_post_valid_token, bytes(login_url, "utf-8")
        )
        # Check that the password has been changed
        self.assertFalse(
            self.client.login(
                username=self.admin_user_data["email"],
                password=self.admin_user_data["password"],
            )
        )
        self.assertTrue(
            self.client.login(
                username=self.admin_user_data["email"],
                password=new_password["new_password1"],
            )
        )

    def test_password_reset_confirm_invalid_token(self):
        # With an invalid token user can acces to the get page
        token = "123tokennotgood"
        uid_user = urlsafe_base64_encode(force_bytes(404))
        response_get_invalid_token = self.client.get(
            reverse(
                "users:password_reset_confirm",
                kwargs={"uidb64": uid_user, "token": token},
            ),
            follow=True,
        )
        self.assertEqual(response_get_invalid_token.status_code, 404)
