from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=60)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return " ".join(self.text.split()[:5]) + ("..." if len(self.text.split()) > 5 else "")

    # Fałszywa zmiana do commita pod merge z głównym branchem Lab 3 Zad 11