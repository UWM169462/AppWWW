from django.contrib import admin
from .models import Category, Topic, Post

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic_category', 'created_at', 'created_by']
    readonly_fields = ['created_at']
    list_filter = ['topic__category', 'topic', 'created_by']
    prepopulated_fields = {"slug": ("title",)}

    @admin.display(description="Topic (Category)")
    def topic_category(self, obj):
        return f"{obj.topic.name} {obj.topic.category.name}"
    topic_category.admin_order_field = 'topic__name'
    topic_category.short_description = 'Topic (Category)'



# # dla przykładowej klasy
# class PersonAdmin(admin.ModelAdmin):
#     # zmienna list_display przechowuje listę pól, które mają się wyświetlać w widoku listy danego modelu w panelu administracynym
#     list_display = ['name', 'shirt_size']
#
# # ten obiekt też trzeba zarejestrować w module admin
# admin.site.register(Person, PersonAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Topic, TopicAdmin)

# Fałszywa zmiana do commita pod merge z głównym branchem do Lab 3 Zad 11