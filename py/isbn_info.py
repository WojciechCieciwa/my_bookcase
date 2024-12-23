import requests

# API Open Library
url = "https://openlibrary.org/search.json?q=python"

# Wysłanie zapytania
response = requests.get(url)

# Sprawdzenie, czy zapytanie zakończyło się sukcesem
if response.status_code == 200:
    data = response.json()

    # Wyświetlenie tytułów książek
    for doc in data['docs'][:5]:  # Pierwsze 5 książek
        print(f"Tytuł: {doc.get('title')}, Autor: {doc.get('author_name', ['Nieznany autor'])[0]}")
else:
    print("Błąd podczas pobierania danych.")
