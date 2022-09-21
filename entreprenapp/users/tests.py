from django.contrib.auth import get_user_model
from django.test import TestCase


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
