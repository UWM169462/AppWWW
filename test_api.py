import requests

BASE = "http://127.0.0.1:8000/api"

print("=" * 50)
print("LAB 6 - TESTY API")
print("=" * 50)

# TEST 1: Pobranie tokena
print("\n✓ TEST 1: Pobranie tokena")
r = requests.post(
    f"{BASE}/auth/token/",
    json={"username": "admin", "password": "a1d2m3i4n5"}
)
print(f"  Status: {r.status_code}")
if r.status_code == 200:
    token = r.json()['token']
    print(f"  Token: {token}")
else:
    print(f"  Błąd: {r.json()}")
    exit()

# TEST 2: Lista postów (publiczne)
print("\n✓ TEST 2: Lista postów (publiczne)")
r = requests.get(f"{BASE}/posts/")
print(f"  Status: {r.status_code}")
print(f"  Postów: {len(r.json())}")

# TEST 3: Posty użytkownika (Basic Auth)
print("\n✓ TEST 3: Posty użytkownika (Basic Auth)")
r = requests.get(
    f"{BASE}/users/posts/",
    auth=("admin", "a1d2m3i4n5")
)
print(f"  Status: {r.status_code}")
print(f"  Postów: {len(r.json())}")

# TEST 4: Topiki kategorii (Token)
print("\n✓ TEST 4: Topiki kategorii (Token)")
r = requests.get(
    f"{BASE}/categories/1/topics/",
    headers={"Authorization": f"Token {token}"}
)
print(f"  Status: {r.status_code}")
print(f"  Topików: {len(r.json())}")

# TEST 5: Spróbuj DELETE bez tokena (powinno być 403)
print("\n✓ TEST 5: DELETE bez tokena (oczekiwany error 403)")
r = requests.delete(f"{BASE}/posts/1/delete/")
print(f"  Status: {r.status_code} (oczekiwany 403)")

# TEST 6: DELETE z tokenem
print("\n✓ TEST 6: DELETE z tokenem")
r = requests.delete(
    f"{BASE}/posts/999/delete/",  # ID które nie istnieje
    headers={"Authorization": f"Token {token}"}
)
print(f"  Status: {r.status_code} (404 OK - posta nie ma)")

print("\n" + "=" * 50)
print("✓ WSZYSTKIE TESTY ZAKOŃCZONE")
print("=" * 50)