from django.test import TestCase
from account.models import Account

# Create your tests here.
class AccountTestCase(TestCase):
    def setUp(self):
        Account.objects.create(username="django", password="django123")

    def test_login_as_correct_username_password(self):
        self.assertTrue(Account.objects.login("django", "django123"))

    def test_login_as_incorrect_username_password(self):
        self.assertFalse(Account.objects.login("django", "xxxxxxxxx"))

    def test_register_with_valid_username_password(self):
        self.assertTrue(Account.objects.register("abcdef", "123456"))

    def test_register_with_registered_username(self):
        self.assertFalse(Account.objects.register("django", "123456"))

    def test_register_with_username_less_then_6_chars(self):
        self.assertFalse(Account.objects.register("abc", "123456"))

    def test_register_with_password_less_then_6_chars(self):
        self.assertFalse(Account.objects.register("django", "123"))
