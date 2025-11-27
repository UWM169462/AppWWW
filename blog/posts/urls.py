from django.urls import path
from . import api_views
from . import views
from .views import CategoryListProtected, CategoryDetailProtected

urlpatterns = [

    # Endpointy Auth
    path('auth/token/', views.get_token, name='get_token'),
    path('auth/user-token/', views.get_current_user_token, name='user_token'),

    # Endpointy Kategorii
    path('categories/', api_views.category_list, name='category_list'),
    path('categories/search/', api_views.category_search, name='category_search'),
    path('categories/<int:pk>/', api_views.category_detail, name='category_detail'),
    path('categories/<int:category_id>/topics/', views.category_topics, name='category_topics'),
    path('categories/<int:pk>/detail-protected/', views.category_detail_with_permission, name='category_detail_protected'),
    path('api/categories/protected/', CategoryListProtected.as_view(), name='category_list_protected'),
    path('api/categories/<int:pk>/protected/', CategoryDetailProtected.as_view(), name='category_detail_protected'),

    # Endpointy tematów
    path('topics/', api_views.topic_list, name='topic_list'),
    path('topics/search/', api_views.topic_search, name='topic_search'),
    path('topics/<int:pk>/', api_views.topic_detail, name='topic_detail'),

    # Endpointy postów
    path('posts/', api_views.post_list, name='post_list'),
    path('posts/<int:pk>/', api_views.post_detail, name='post_detail'),
    path('posts/search/', api_views.post_search, name='post_search'),
    path('posts/<int:pk>/update/', views.post_update, name='post_update'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('posts/create/', views.post_create, name='post_create'),
    path('users/posts/', views.user_posts, name='user_posts'),
    path('posts/<int:pk>/update-protected/', views.post_update_with_permission, name='post_update_protected'),
]