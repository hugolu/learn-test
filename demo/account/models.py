from django.db import models

# Create your models here.
class AccountManager(models.Manager):
    def create(self, username, password):
        account = super(AccountManager, self).create(username=username, password=password)

        return account

    def verify(self, username, password):
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
        if len(username) <= 5 or len(password) <= 5:
            return False

        if self.exist(username=username):
            return False

        self.create(username, password)
        return True

class Account(models.Model):
    username = models.CharField(u'username', max_length=20)
    password = models.CharField(u'password', max_length=20)

    objects = AccountManager()
