import json

class DatabaseTextInterface:
    def __init__(self, db_manager):
        """
        Initializes the text interface with a given DatabaseManager instance.
        """
        self.db = db_manager

    def run(self):
        """
        Main loop: continuously display the main menu until the user exits.
        """
        while True:
            self.main_menu()

    def main_menu(self):
        """
        Displays the main menu and routes the user’s choice.
        """
        print("\n==== Main Menu ====")
        print("1. Search for a book")
        # print("2. Search for a series")
        print("3. Undelete a book")
        # print("4. Undelete a series")
        print("5. Display update history")
        print("6. Exit")
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            self.search_books_menu()
        # elif choice == "2":
        #    self.search_series_menu()
        elif choice == "3":
            self.undelete_book_menu()
        # elif choice == "4":
        #     self.undelete_series_menu()
        elif choice == "5":
            self.display_update_history()
        elif choice == "6":
            print("Exiting. Goodbye!")
            self.db.close()
            exit(0)
        else:
            print("Invalid choice. Please try again.")

    def search_books_menu(self):
        """
        Prompts the user for a search term, displays matching (active) books
        with pagination, and allows selection for further actions.
        """
        search_term = input("\nEnter search term for books: ").strip()
        # Assuming db.search_books returns a list of book dictionaries.
        # It is expected that books with status "deleted" are filtered out.
        books = self.db.search_books(search_term)
        if not books:
            print("No books found matching the search term.")
            return
        
        page = 0
        while True:
            start = page * 10
            end = start + 10
            page_books = books[start:end]
            if not page_books:
                print("No more books to display.")
                break
            # print(page_books)
            print(f"\n--- Books (Page {page+1}) ---")
            # print(f"{page_books}")
            for i, book in enumerate(page_books):
                book_dict = {
                    "id": book[0],
                    "authors": json.loads(book[1]) if book[1] else [],
                    "title": book[2],
                    "edition": book[3],
                    "language": book[4],
                    "location": book[5],
                    "publisher": book[6],
                    "release_year": book[7],
                    "isbn_13": book[8],
                    "pages": book[9],
                    "tags": json.loads(book[10]) if book[10] else [],
                    "description": book[11],
                    "status": book[12]
                    }
                print(f"{i+1}. {self.display_book_briefly(book_dict)}")

            print("\nn: next page, p: previous page, s: select a book, b: back to main menu")
            action = input("Your choice: ").strip().lower()

            if action == 'n':
                if end < len(books):
                    page += 1
                else:
                    print("This is the last page.")
            elif action == 'p':
                if page > 0:
                    page -= 1
                else:
                    print("Already at the first page.")
            elif action == 's':
                try:
                    selection = int(input("Enter the number of the book to select: "))
                    if 1 <= selection <= len(page_books):
                        self.book_details_menu(page_books[selection - 1])
                        books = self.db.search_books(search_term)
                        if not books:
                            print("No books found matching the search term.")
                            return
                    else:
                        print("Invalid selection number.")
                except ValueError:
                    print("Please enter a valid number.")
            elif action == 'b':
                break
            else:
                print("Invalid option. Please try again.")

    def display_book_briefly(self, book_dict):
        """
        print(f'{book_dict["id"]}. {book_dict["authors"]} ({book_dict["release_year"]}) \"{book_dict["title"]}\". {book_dict["publisher"]}. {book_dict["isbn_13"]}. [{book_dict["status"]}]')
        """
        return (f'{", ".join(book_dict["authors"])}. \"{book_dict["title"]}\". {book_dict["publisher"]}. {book_dict["isbn_13"]}. {book_dict["release_year"]}. [{book_dict["status"]}].')


    def parse_string_to_list(self, string_with_brackets):
        string_processed = string_with_brackets.strip(" ").strip("[]")
        string_list = string_processed.split(",")
        string_list_stripped = [s.strip('" ') for s in string_list]
        return string_list_stripped

    def book_details_menu(self, book):
        """
        Displays details for the selected book and provides options to edit or delete.
        """
        book_dict = {
            "id": book[0],
            "authors": ", ".join(json.loads(book[1]) if book[1] else []),
            "title": book[2],
            "edition": book[3],
            "language": book[4],
            "location": book[5],
            "publisher": book[6],
            "release_year": book[7],
            "isbn_13": book[8],
            "pages": book[9],
            "tags": ", ".join(json.loads(book[10]) if book[10] else []),
            "description": book[11],
            "status": book[12]
        }
        print("\n==== Book Details ====")
        for key in book_dict:
            if (isinstance(book_dict[key], dict)) or (isinstance(book_dict[key], list)):
                print(f"{key}: {', '.join(book_dict[key])}")
            else:
                print(f"{key}: {book_dict[key]}")
        print("\ne: edit, d: mark as deleted, b: back")
        choice = input("Select an option: ").strip().lower()
        if choice == 'e':
            self.edit_book_menu(book_dict)
        elif choice == 'd':
            self.delete_book(book_dict)
        elif choice == 'b':
            return
        else:
            print("Invalid option.")

    def edit_book_menu(self, book):
        """
        Allows the user to edit a book. For each field, if the user enters a new value,
        it is used; otherwise the existing value is retained.
        """
        print("\n==== Edit Book ====")
        print("Leave a field blank to keep its current value.")

        updates_fields = {
            "authors": "Authors (comma separated)",
            "title": "Title",
            "edition": "Edition",
            "language": "Language",
            "location": "Location",
            "publisher": "Publisher",
            "release_year": "Release Year",
            "isbn_13": "ISBN 13",
            "pages": "Number of pages",
            "tags": "Tags (comma separated)",
            "description": "Description",
            "status": "Status",
        }

        updates = {}
        for field_name in updates_fields.keys():
            new_field_value = input(f"{updates_fields[field_name]} ({book.get(field_name, '')}): ") or book.get(field_name)
            if new_field_value != book.get(field_name, ''):
                if field_name in ['authors', 'tags']:
                    updates[field_name] = self.list_to_string(new_field_value)
                else:
                    updates[field_name] = new_field_value

        # new_authors = input(f"Authors (comma separated) ({book.get('authors', '')}): ") or book.get('authors')
        # new_title = input(f"Title ({book.get('title', '')}): ") or book.get('title')
        # new_edition = input(f"Edition ({book.get('edition', '')}): ") or book.get('edition')
        # new_language = input(f"Language ({book.get('language', '')}): ") or book.get('language')
        # new_location = input(f"Location ({book.get('location', '')}): ") or book.get('location')
        # new_publisher = input(f"Publisher ({book.get('publisher', '')}): ") or book.get('publisher')
        # new_release_year = input(f"Release Year ({book.get('release_year', '')}): ") or book.get('release_year')
        # new_isbn_13 = input(f"ISBN 13 ({book.get('isbn_13', '')}): ") or book.get('isbn_13')
        # new_pages = input(f"Number of pages ({book.get('pages', '')}): ") or book.get('pages')
        # new_tags = input(f"Tags (comma separated) ({book.get('tags', '')}): ") or book.get('tags')
        # new_description = input(f"Description ({book.get('description', '')}): ") or book.get('description')
        # new_status = input(f"Status ({book.get('status', '')}): ") or book.get('status')

        # updates = {
        #     "authors": self.list_to_string(new_authors),
        #     "title": new_title,
        #     "edition": new_edition,
        #     "language": new_language,
        #     "location": new_location,
        #     "publisher": new_publisher,
        #     "release_year": new_release_year,
        #     "isbn_13": new_isbn_13,
        #     "pages": str(new_pages),
        #     "tags": self.list_to_string(new_tags),
        #     "description": new_description,
        #     "status": new_status,
        # }
        # print (f"edit_book_menu: updates: {updates}")
        updates_summary = self.db.update_book(book['id'], updates, updated_by="user")
        if updates_summary:
            print(f"Book updated: {updates_summary}")
        else:
            print(f"No changes, book not updated.")

    def list_to_string(self, comma_delimited_string):
        # print(comma_string)
        items_list = comma_delimited_string.split(",")
        # items_list = comma_string
        if not isinstance(items_list, list) or not items_list:
            return json.dumps({})
        cleaned_list = [item.strip() for item in items_list if isinstance(item, str)]
        return json.dumps(cleaned_list)    


    def delete_book(self, book_dict):
        """
        Marks a book as deleted (for example by updating its status).
        """
        confirmation = input(f"Are you sure you want to mark '{book_dict['title']}' as deleted? (y/n): ").strip().lower()
        if confirmation == 'y':
            self.db.delete_book(book_dict['id'], updated_by="user")
            print("Book marked as deleted.")
        else:
            print("Operation canceled.")

    def undelete_book_menu(self):
        """
        Displays a list of deleted books (paged by 10) and allows the user to undelete one.
        Assumes that the DatabaseManager provides a method get_deleted_books().
        """
        try:
            deleted_books = self.db.get_deleted_books()
        except AttributeError:
            print("DatabaseManager does not support retrieving deleted books.")
            return

        if not deleted_books:
            print("No deleted books found.")
            return

        page = 0
        while True:
            start = page * 10
            end = start + 10
            page_books = deleted_books[start:end]
            if not page_books:
                print("No more deleted books to display.")
                break

            print(f"\n--- Deleted Books (Page {page+1}) ---")
            for idx, book in enumerate(page_books, start=1):
                print(f"{idx}. {book['title']} (ID: {book['id']})")
            print("\nn: next page, p: previous page, u: undelete a book, b: back")
            action = input("Your choice: ").strip().lower()

            if action == 'n':
                if end < len(deleted_books):
                    page += 1
                else:
                    print("This is the last page.")
            elif action == 'p':
                if page > 0:
                    page -= 1
                else:
                    print("Already at the first page.")
            elif action == 'u':
                try:
                    selection = int(input("Enter the number of the book to undelete: "))
                    if 1 <= selection <= len(page_books):
                        self.undelete_book(page_books[selection - 1])
                        # Optionally, remove the book from the list once undeleted.
                        deleted_books.remove(page_books[selection - 1])
                    else:
                        print("Invalid selection number.")
                except ValueError:
                    print("Please enter a valid number.")
            elif action == 'b':
                break
            else:
                print("Invalid option.")

    def undelete_book(self, book):
        """
        Undeletes a book by updating its status to 'active' (or another appropriate value).
        """
        self.db.update_book(book['id'], {"status": "active"}, updated_by="user")
        print(f"Book '{book['title']}' has been undeleted.")

    def search_series_menu(self):
        """
        Similar to search_books_menu but for book series.
        Assumes that the DatabaseManager provides a search_series(term) method.
        """
        search_term = input("\nEnter search term for series: ").strip()
        try:
            series_list = self.db.search_series(search_term)
        except AttributeError:
            print("DatabaseManager does not support series search.")
            return

        if not series_list:
            print("No series found matching the search term.")
            return

        page = 0
        while True:
            start = page * 10
            end = start + 10
            page_series = series_list[start:end]
            if not page_series:
                print("No more series to display.")
                break

            print(f"\n--- Series (Page {page+1}) ---")
            for idx, series in enumerate(page_series, start=1):
                print(f"{idx}. {series['title']} (ID: {series['id']})")
            print("\nn: next page, p: previous page, s: select a series, b: back")
            action = input("Your choice: ").strip().lower()

            if action == 'n':
                if end < len(series_list):
                    page += 1
                else:
                    print("This is the last page.")
            elif action == 'p':
                if page > 0:
                    page -= 1
                else:
                    print("Already at the first page.")
            elif action == 's':
                try:
                    selection = int(input("Enter the number of the series to select: "))
                    if 1 <= selection <= len(page_series):
                        self.series_details_menu(page_series[selection - 1])
                    else:
                        print("Invalid selection number.")
                except ValueError:
                    print("Please enter a valid number.")
            elif action == 'b':
                break
            else:
                print("Invalid option.")

    def series_details_menu(self, series):
        """
        Displays details for the selected series and provides options to edit or delete.
        """
        print("\n==== Series Details ====")
        for key, value in series.items():
            print(f"{key}: {value}")
        print("\ne: edit, d: mark as deleted, b: back")
        choice = input("Select an option: ").strip().lower()
        if choice == 'e':
            self.edit_series_menu(series)
        elif choice == 'd':
            self.delete_series(series)
        elif choice == 'b':
            return
        else:
            print("Invalid option.")

    def edit_series_menu(self, series):
        """
        Allows the user to edit series details. Expects a comma-separated list of book IDs.
        """
        print("\n==== Edit Series ====")
        new_title = input(f"Title ({series.get('title', '')}): ") or series.get('title')
        books_current = ', '.join(str(b) for b in series.get('books', []))
        new_books = input(f"Books (comma separated IDs) ({books_current}): ")
        if new_books:
            try:
                new_books = [int(x.strip()) for x in new_books.split(',')]
            except ValueError:
                print("Invalid book IDs. Keeping current list.")
                new_books = series.get('books', [])
        else:
            new_books = series.get('books', [])

        # Here we assume update_series accepts the updated title and books list.
        self.db.update_series(series['id'], title=new_title, books=new_books)
        print("Series updated.")

    def delete_series(self, series):
        """
        Marks a series as deleted. This assumes that the DatabaseManager has a delete_series method.
        """
        confirmation = input(f"Are you sure you want to mark series '{series['title']}' as deleted? (y/n): ").strip().lower()
        if confirmation == 'y':
            try:
                self.db.delete_series(series['id'], updated_by="user")
                print("Series marked as deleted.")
            except AttributeError:
                print("DatabaseManager does not support deleting series.")
        else:
            print("Operation canceled.")

    def undelete_series_menu(self):
        """
        Displays a paginated list of deleted series and allows the user to undelete one.
        Assumes that the DatabaseManager provides get_deleted_series().
        """
        try:
            deleted_series = self.db.get_deleted_series()
        except AttributeError:
            print("DatabaseManager does not support retrieving deleted series.")
            return

        if not deleted_series:
            print("No deleted series found.")
            return

        page = 0
        while True:
            start = page * 10
            end = start + 10
            page_series = deleted_series[start:end]
            if not page_series:
                print("No more deleted series to display.")
                break

            print(f"\n--- Deleted Series (Page {page+1}) ---")
            for idx, series in enumerate(page_series, start=1):
                print(f"{idx}. {series['title']} (ID: {series['id']})")
            print("\nn: next page, p: previous page, u: undelete a series, b: back")
            action = input("Your choice: ").strip().lower()

            if action == 'n':
                if end < len(deleted_series):
                    page += 1
                else:
                    print("This is the last page.")
            elif action == 'p':
                if page > 0:
                    page -= 1
                else:
                    print("Already at the first page.")
            elif action == 'u':
                try:
                    selection = int(input("Enter the number of the series to undelete: "))
                    if 1 <= selection <= len(page_series):
                        self.undelete_series(page_series[selection - 1])
                        deleted_series.remove(page_series[selection - 1])
                    else:
                        print("Invalid selection number.")
                except ValueError:
                    print("Please enter a valid number.")
            elif action == 'b':
                break
            else:
                print("Invalid option.")

    def undelete_series(self, series):
        """
        Undeletes a series. Depending on your implementation, this may involve
        updating its status to active.
        """
        # Here we assume that undeleting is achieved by updating the series (or calling a dedicated method)
        self.db.update_series(series['id'], title=series['title'], books=series['books'])
        print(f"Series '{series['title']}' has been undeleted.")

    def display_update_history(self):
        """
        Displays the history of book updates. This assumes that the DatabaseManager
        provides a get_update_history() method.
        """
        try:
            history = self.db.get_update_history()
        except AttributeError:
            print("DatabaseManager does not support update history retrieval.")
            return

        if not history:
            print("No update history available.")
        else:
            print("\n==== Update History ====")
            for update in history:
                # Update records could be dictionaries or objects; adjust as needed.
                print(update)
        input("\nPress Enter to return to the main menu.")
