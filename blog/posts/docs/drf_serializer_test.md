### Test 1: CategorySerializer

```python
from posts.models import Category
from posts.serializers import CategorySerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io

print("TEST 1: CategorySerializer (ModelSerializer)")

print("\nTworzenie kategorii testowej...")
category = Category.objects.create(
    name='REST API Test',
    description='Testing ModelSerializer'
)
print(f"Kategoria utworzona: {category.name} (ID: {category.id})")

print("\nSerializacja danych kategorii...")
serializer = CategorySerializer(category)
print(f"Dane serializera:")
for key, value in serializer.data.items():
    print(f"  - {key}: {value}")

print("\nKonwersja do JSON...")
content = JSONRenderer().render(serializer.data)
print(f"JSON:\n  {content.decode('utf-8')}")

# Deserializacja
print("\nParsowanie i walidacja JSON...")
stream = io.BytesIO(content)
data = JSONParser().parse(stream)
deserializer = CategorySerializer(data=data)

if deserializer.is_valid():
    print(f"Walidacja pomyślna!")
    updated = deserializer.save()
    print(f"Dane zaktualizowane: {updated.name}")
else:
    print(f"Błędy walidacji: {deserializer.errors}")

# Czyszczenie
category.delete()
print("\n Dane testowe usunięte")
```

### Test 2: PostSerializer 

```python
from posts.models import Post, Topic, Category
from posts.serializers import PostSerializer
from django.contrib.auth import get_user_model
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io

User = get_user_model()

print("TEST 2: PostSerializer")

print("\nTworzenie danych testowych...")
category = Category.objects.create(name='Blog', description='Blog posts')
topic = Topic.objects.create(name='Python', category=category)
user = User.objects.first() or User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)
print(f"Kategoria: {category.name}")
print(f"Temat: {topic.name}")
print(f"Użytkownik: {user.username}")

print("\nTworzenie posta testowego...")
post = Post.objects.create(
    title='Django Rest Framework Introduction',
    text='A comprehensive guide to DRF and serializers...',
    topic=topic,
    slug='drf-introduction',
    created_by=user
)
print(f"Post utworzony: {post.title} (ID: {post.id})")

print("\nSerializacja posta z powiązanymi danymi...")
serializer = PostSerializer(post)
print(f"✓ Dane serializera:")
for key, value in serializer.data.items():
    print(f"  - {key}: {value}")

print("\nKonwersja do JSON...")
content = JSONRenderer().render(serializer.data)
json_str = content.decode('utf-8')
print(f"JSON (pierwsze 200 znaków):")
print(f"  {json_str[:200]}...")

# 4. Deserializacja
print("\nParsowanie i walidacja JSON...")
stream = io.BytesIO(content)
data = JSONParser().parse(stream)

# Usuń read-only pola do re-save
data_for_update = {k: v for k, v in data.items() 
                   if k not in ['id', 'created_at', 'updated_at', 'created_by_username', 'topic_name', 'category_name']}
data_for_update['created_by'] = user.id

deserializer = PostSerializer(data=data_for_update)

if deserializer.is_valid():
    print(f"Walidacja pomyślna!")
else:
    print(f"Błędy walidacji: {deserializer.errors}")

# Czyszczenie
post.delete()
topic.delete()
category.delete()
print("\nDane testowe usunięte")
```
