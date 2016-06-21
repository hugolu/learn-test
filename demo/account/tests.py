from django.test import TestCase
from account.models import Account

# Create your tests here.
class AccountTestCase(TestCase):

    def setUp(self):
        Account.objects.create(username="django", password="123456")

    ## test verify
    def test_verify_with_correct_username_password(self):
        self.assertTrue(Account.objects.verify("django", "123456"))

    def test_verify_with_incorrect_username(self):
        self.assertFalse(Account.objects.verify("foobar", "123456"))

    def test_verify_with_incorrect_password(self):
        self.assertFalse(Account.objects.verify("django", "foobar"))

    ## test exist
    def test_exist_with_registered_uername(self):
        self.assertTrue(Account.objects.exist("django"))

    def test_exist_with_unregistered_username(self):
        self.assertFalse(Account.objects.exist("foobar"))

    ## test register
    def test_register_with_valid_username_password(self):
        self.assertTrue(Account.objects.register("foobar", "foobar"))

    def test_register_with_username_less_then_6_chars(self):
        self.assertFalse(Account.objects.register("abc", "123456"))

    def test_register_with_password_less_then_6_chars(self):
        self.assertFalse(Account.objects.register("django", "123"))

    def test_register_with_registered_username(self):
        self.assertFalse(Account.objects.register("django", "123456"))
