from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(u'Name', max_length=50)

    def __str__(self):
        return self.name

class Article(models.Model):
    content = models.TextField(u'Content')
    title = models.CharField(u'Title', max_length=50)
    category = models.ForeignKey('Category', blank=True, null=True)

    def __str__(self):
        return self.title
