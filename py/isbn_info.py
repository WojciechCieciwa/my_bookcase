import requests

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
            
            print(book)
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

def get_book_info2(isbn):
    # URL do Google Books API
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    
    ISBN_field_list = {}

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
            ISBN_field_list["Okładka"]         = thumbnail
            ISBN_field_list["title"]           = title
            ISBN_field_list["Autorzy"]         = authors
            ISBN_field_list["Wydawca"]         = publisher
            ISBN_field_list["Data publikacji"] = published_date
            ISBN_field_list["Liczba stron"]    = page_count
            ISBN_field_list["Język"]           = language
            ISBN_field_list["Opis"]            = description
            ISBN_field_list["status"]          = "OK"
        else:
            ISBN_field_list["status"] = "ERROR: Nie znaleziono książki o podanym ISBN."
    else:
        ISBN_field_list["status"] = "ERROR: Błąd w połączeniu z API."
    return ISBN_field_list

# Przykładowe wywołanie funkcji
#isbn = input("Podaj numer ISBN książki: ")
#print(get_book_info2(isbn))
#get_book_info(isbn)
