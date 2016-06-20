from django.db import models

# Create your models here.
class AccountManager(models.Manager):
    def create(self, username, password):
        account = super(AccountManager, self).create(username=username, password=password)
        return account

    def login(self, username, password):
        try:
            account = self.get(username=username, password=password)
        except self.model.DoesNotExist:
            account = None
        return (account is not None)

    def exist(self, username):
        try:
            account = self.get(username=username)
        except self.model.DoesNotExist:
            account = None
        return (account is not None)

    def register(self, username, password):
        if len(username) > 5 and len(password) > 5:
            if self.exist(username) == False:
                self.create(username, password)
                return True
        return False

class Account(models.Model):
    username = models.CharField(u'username', max_length=20)
    password = models.CharField(u'password', max_length=20)
    email = models.CharField(u'email', max_length=40)
    phone = models.CharField(u'phone', max_length=40)

    objects = AccountManager()
