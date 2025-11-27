from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from django.http import Http404

from .models import Category, Topic, Post
from .serializers import CategorySerializer, TopicSerializer, PostSerializer
from .permissions import CustomDjangoModelPermissions


class CategoryListProtected(APIView):
    """
    Class-based view dla listy kategorii z DjangoModelPermissions.

    - GET: sprawdza uprawnienie posts.view_category
    - POST: sprawdza uprawnienie posts.add_category
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        """Wymagane dla DjangoModelPermissions"""
        return Category.objects.all()

    def get(self, request, format=None):
        """GET - sprawdza uprawnienie view_category"""
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """POST - sprawdza uprawnienie add_category"""
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailProtected(APIView):
    """
    Class-based view dla szczegółów kategorii z DjangoModelPermissions.

    - GET: sprawdza uprawnienie posts.view_category
    - PUT: sprawdza uprawnienie posts.change_category
    - DELETE: sprawdza uprawnienie posts.delete_category
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        """Wymagane dla DjangoModelPermissions"""
        return Category.objects.all()

    def get_object(self, pk):
        """Pobierz obiekt lub zwróć 404"""
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404("Kategoria nie znaleziona")

    def get(self, request, pk, format=None):
        """GET - sprawdza uprawnienie view_category"""
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """PUT - sprawdza uprawnienie change_category"""
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """DELETE - sprawdza uprawnienie delete_category"""
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# ===== AUTHENTICATION ENDPOINTS =====

@api_view(['POST'])
def get_token(request):
    """
    Endpoint do otrzymania tokena autentykacji.
    Wymaga username i password w JSON.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_current_user_token(request):
    """
    Pobranie tokena dla aktualnie zalogowanego użytkownika.
    """
    token, created = Token.objects.get_or_create(user=request.user)
    return Response({'token': token.key, 'user': request.user.username})


# ===== POST ENDPOINTS =====

@api_view(['GET'])
def post_list(request):
    """
    Lista wszystkich postów.
    Dostęp publiczny (bez uwierzytelnienia).
    """
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def post_detail(request, pk):
    """
    Szczegóły pojedynczego posta.
    Dostęp publiczny.
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def post_create(request):
    """
    Tworzenie nowego posta.
    Wymaga uwierzytelnienia (sesja lub basic auth).
    """
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def post_update(request, pk):
    """
    Aktualizacja posta.
    Wymaga uwierzytelnienia (sesja lub basic auth).
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_delete(request, pk):
    """
    Usunięcie posta.
    Wymaga uwierzytelnienia TOKEN!
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def user_posts(request):
    """
    Zwraca posty dla aktualnie zalogowanego użytkownika.
    Wymaga uwierzytelnienia.
    """
    posts = Post.objects.filter(created_by=request.user)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


# ===== CATEGORY ENDPOINTS =====

@api_view(['GET'])
def category_list(request):
    """
    Lista wszystkich kategorii.
    Dostęp publiczny.
    """
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def category_detail(request, pk):
    """
    Szczegóły kategorii.
    Dostęp publiczny.
    """
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_topics(request, category_id):
    """
    Topiki dla podanej kategorii.
    Dostęp tylko do odczytu i tylko z TOKEN!
    URL: /categories/<id>/topics/
    """
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    topics = Topic.objects.filter(category=category)
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)


# ===== TOPIC ENDPOINTS =====

@api_view(['GET'])
def topic_list(request):
    """
    Lista wszystkich topików.
    Dostęp publiczny.
    """
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def topic_detail(request, pk):
    """
    Szczegóły topiku.
    Dostęp publiczny.
    """
    try:
        topic = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TopicSerializer(topic)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def category_detail_with_permission(request, pk):
    """
    Widok szczegółów kategorii z kontrolą uprawnienia view_category.
    Wymaga uwierzytelnienia.
    URL: /categories/<int:pk>/detail-protected/
    """
    # Sprawdzenie uprawnienia
    if not request.user.has_perm('posts.view_category'):
        raise PermissionDenied("Nie masz uprawnienia do przeglądania kategorii")

    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(
            {'error': f'Kategoria o id={pk} nie istnieje'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = CategorySerializer(category)
    return Response(serializer.data)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def post_update_with_permission(request, pk):
    """
    Edycja posta z kontrolą uprawnień:
    - Autor zawsze może edytować swój post
    - Inni użytkownicy mogą edytować obcy post tylko jeśli mają uprawnienie 'can_edit_others_posts'

    URL: /posts/<int:pk>/update-protected/
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(
            {'error': f'Post o id={pk} nie istnieje'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Sprawdzenie uprawnień
    is_author = post.created_by == request.user
    has_moderator_perm = request.user.has_perm('posts.can_edit_others_posts')

    if not is_author and not has_moderator_perm:
        raise PermissionDenied(
            "Nie masz uprawnień do edycji tego posta. "
        )

    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)