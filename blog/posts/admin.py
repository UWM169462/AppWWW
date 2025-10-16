from django.contrib import admin

# Register your models here.

# modele musimy zaimportować
from .models import Category, Topic

# a następnie zarejestrować (pokazano najprostszy przypadek)
admin.site.register(Category)
admin.site.register(Topic)