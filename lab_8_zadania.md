# Lab 8 – Zadania GraphQL

## 1. Podstawowe zapytania

### 1.1. Lista wszystkich kategorii (ID, nazwa, opis)

```graphql
{
  allCategories {
    id
    name
    description
  }
}
```
---

### 1.2. Lista wszystkich postów z tematem i kategorią

```graphql
query {
  allPosts {
    id
    title
    slug
    topic {
      id
      name
      category {
        id
        name
      }
    }
    createdBy {
      id
      username
    }
    createdAt
    updatedAt
  }
}
```
---

### 1.3. Pojedyncza kategoria po ID

```graphql
query {
  categoryById(id: 1) {
    id
    name
    description
  }
}
```
---

### 1.4. Pojedynczy temat po ID

```graphql
query {
  topicById(id: 1) {
    id
    name
    category {
      id
      name
    }
    created
  }
}
```
---

### 1.5. Pojedynczy post po ID

```graphql
query {
  postById(id: 1) {
    id
    title
    text
    slug
    topic {
      name
      category {
        name
      }
    }
    createdBy {
      username
    }
    createdAt
    updatedAt
  }
}
```
---

## 2. Dodatkowe resolvery (Zadanie 2)

### 2.1. Kategorie zawierające fragment nazwy (bez względu na wielkość liter)

```graphql
query {
  categoriesByNameContains(substr: "nowa") {
    id
    name
    description
  }
}
```
---

### 2.2. Liczba postów danego użytkownika

```graphql
query {
  postsCountByUser(username: "admin")
}
```
---

### 2.3. Posty w danej kategorii (po nazwie kategorii)

```graphql
query {
  postsByCategoryName(categoryName: "REST API test") {
    id
    title
    topic {
      name
      category {
        name
      }
    }
    createdBy {
      username
    }
    createdAt
  }
}
```
---

## 3. Mutacje dla modelu Post (Zadanie 3)

### 3.1. Utworzenie nowego posta

```graphql
mutation {
  createPost(
    title: "Walcząc z Pythonem"
    text: "Treść posta testowego utworzonego za pośrednictwem interfejsu GraphQL, zamiast API przez Python"
    topicId: 1
    slug: "walczac-z-pythonem"
    createdById: 2
  ) {
    post {
      id
      title
      slug
      createdBy {
        id
        username
      }
      topic {
        id
        name
      }
      createdAt
    }
  }
}
```
---

### 3.2. Aktualizacja istniejącego posta (zmieniana kategorii)

```graphql
mutation {
  updatePost(
    id:5
    topicId: 2
  ) {
    post {
      id
      title
      text
      updatedAt
      createdBy {
        username
      }
    }
  }
}
```

**Uagi:**
- Post o danym ID musi istnieć
- Nowy `slug` musi być unikalny

---

### 3.3. Usunięcie posta

```graphql
mutation {
  deletePost(id: 6) {
    ok
  }
}
```

**Uwagi:**
- Post o danym ID musi istnieć
- Operacja jest nieodwracalna
-post testowy został stworzony poleceniem:
```graphql
mutation {
  createPost(
    title: "spam"
    text: "spam"
    topicId: 1
    slug: "spam"
    createdById: 2
  ) {
    post {
      id
    }
  }
}
```