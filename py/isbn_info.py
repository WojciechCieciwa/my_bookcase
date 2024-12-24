import requests

## API Open Library
#url = "https://openlibrary.org/search.json?q=python"#
#
# Wysłanie zapytania
#response = requests.get(url)

# Sprawdzenie, czy zapytanie zakończyło się sukcesem
#if response.status_code == 200:
#    data = response.json()#
#
#    # Wyświetlenie tytułów książek
#    for doc in data['docs'][:1]:  # Pierwsze 5 książek
#        print(f"Tytuł: {doc.get('title')}, Autor: {doc.get('author_name', ['Nieznany autor'])[0]}")
#        print(f"{doc.get()}")
#  else:
#    print("Błąd podczas pobierania danych.")
#

def get_book_info(isbn):
    # URL do Google Books API
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    
    # Wykonaj zapytanie HTTP
    response = requests.get(url)
    
    # Sprawdź, czy zapytanie zakończyło się sukcesem
    if response.status_code == 200:
        data = response.json()
        
        # Jeśli książka została znaleziona
        if 'items' in data:
            book = data['items'][0]['volumeInfo']
            
            # Wydobywanie informacji o książce
            title = book.get('title', 'Brak tytułu')
            authors = ', '.join(book.get('authors', ['Brak autorów']))
            publisher = book.get('publisher', 'Brak wydawcy')
            published_date = book.get('publishedDate', 'Brak daty publikacji')
            description = book.get('description', 'Brak opisu')
            page_count = book.get('pageCount', 'Brak liczby stron')
            language = book.get('language', 'Brak języka')
            thumbnail = book.get('imageLinks', {}).get('thumbnail', 'Brak okładki')

            # Wyświetlenie informacji o książce
            print(f"Tytuł: {title}")
            print(f"Autorzy: {authors}")
            print(f"Wydawca: {publisher}")
            print(f"Data publikacji: {published_date}")
            print(f"Liczba stron: {page_count}")
            print(f"Język: {language}")
            print(f"Opis: {description}")
            print(f"Okładka: {thumbnail}")
        else:
            print("Nie znaleziono książki o podanym ISBN.")
    else:
        print("Błąd w połączeniu z API.")

# Przykładowe wywołanie funkcji
isbn = input("Podaj numer ISBN książki: ")
get_book_info(isbn)
