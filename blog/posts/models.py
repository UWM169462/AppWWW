from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()


class Topic(models.Model):
    name = models.CharField(max_length=60)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)