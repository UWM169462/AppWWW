### import potrzebnych danych
```Pyhon
from posts.models import Category, Topic, Post  # Zadanie 10: Import modeli
```

### 1. Wyświetl wszystkie obiekty Category
```Pyhon
Category.objects.all()
```

### 2. Wyświetl obiekt Category z id=3
```Pyhon
Category.objects.get(id=3)
```

### 3. Wyświetl obiekty Category, których nazwa zaczyna się na wybraną literę (np. "A")
```Pyhon
Category.objects.filter(name__startswith="A")
```

### 4. Wyświetl unikalną listę nazw kategorii ze wszystkich tematów (Topic)
```Pyhon
Category.objects.filter(topic__isnull=False).distinct().values_list('name', flat=True)
```

### 5. Wyświetl tytuły postów posortowane alfabetycznie malejąco
```Pyhon
Post.objects.order_by('-title').values_list('title', flat=True)
```

### 6. Dodaj nową instancję Category i zapisz w bazie
```Pyhon
cat = Category.objects.create(name="Nowa kategoria")
cat.save()
```
