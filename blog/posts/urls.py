from django.urls import path
from . import api_views

urlpatterns = [

    # Endpointy Kategorii
    path('categories/', api_views.category_list, name='category_list'),
    path('categories/search/', api_views.category_search, name='category_search'),
    path('categories/<int:pk>/', api_views.category_detail, name='category_detail'),

    # Endpointy tematów
    path('topics/', api_views.topic_list, name='topic_list'),
    path('topics/search/', api_views.topic_search, name='topic_search'),
    path('topics/<int:pk>/', api_views.topic_detail, name='topic_detail'),

    # Endpointy postów
    path('posts/', api_views.post_list, name='post_list'),
    path('posts/<int:pk>/', api_views.post_detail, name='post_detail'),
    path('posts/search/', api_views.post_search, name='post_search'),

]