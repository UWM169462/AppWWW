from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, Topic, Post
from .serializers import CategorySerializer, TopicSerializer, PostSerializer

# KATEGORIA
@api_view(['GET', 'POST'])
def category_list(request):
    # Dodaj do / Wyświetl listę kategorii
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    # Wyświetl/edytuj/usuń jedną
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def category_search(request):
    # Wyświetl kategorie zawierające łańcuch znaków
    search_query = request.query_params.get('name', '').strip()
    # Błąd gdy puste query
    if not search_query:
        return Response(
            {'error': 'Parametr name jest wymagany'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Filtruj po title
    categories = Category.objects.filter(name__icontains=search_query)
    if not categories.exists():
        return Response(
            {'message': f'Nie znaleziono kategorii zawierających "{search_query}"'},
            status=status.HTTP_200_OK
        )
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

# TEMAT
@api_view(['GET', 'POST'])
def topic_list(request):
    # Dodaj do / Wyświetl listę tematów
    if request.method == 'GET':
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def topic_detail(request, pk):
    # Wyświetl/edytuj/usuń jeden
    try:
        topic = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TopicSerializer(topic)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TopicSerializer(topic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        topic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def topic_search(request):
    # Wyświetl tematy zawierające łańcuch znaków
    search_query = request.query_params.get('name', '').strip()
    # Błąd gdy puste query
    if not search_query:
        return Response(
            {'error': 'Parametr name jest wymagany'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Filtruj po title
    topics = Topic.objects.filter(name__icontains=search_query)
    if not topics.exists():
        return Response(
            {'message': f'Nie znaleziono tematów zawierających "{search_query}"'},
            status=status.HTTP_200_OK
        )
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)
# POSTY
@api_view(['GET', 'POST'])
def post_list(request):
    # Dodaj do / Wyświetl listę postów
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    # Wyświetl/edytuj/usuń jeden
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def post_search(request):
    # Wyświetl posty zawierające w nazwie zadany łańcuch znaków
    search_query = request.query_params.get('title', '').strip()
    # Błąd gdy puste query
    if not search_query:
        return Response(
            {'error': 'Parametr title jest wymagany'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Filtruj po title
    posts = Post.objects.filter(title__icontains=search_query)
    if not posts.exists():
        return Response(
            {'message': f'Nie znaleziono postów zawierających "{search_query}"'},
            status=status.HTTP_200_OK
        )
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
