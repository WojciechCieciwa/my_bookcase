Below is an example of a Python class that implements a text‐based interface for the database. In this design, the class (here called `DatabaseTextInterface`) assumes that the provided `DatabaseManager` class (and some extra helper methods such as retrieving deleted items, searching for series, and getting update history) are available. You may need to adjust or implement those extra methods in your actual database manager.

```python
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
        print("2. Search for a series")
        print("3. Undelete a book")
        print("4. Undelete a series")
        print("5. Display update history")
        print("6. Exit")
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            self.search_books_menu()
        elif choice == "2":
            self.search_series_menu()
        elif choice == "3":
            self.undelete_book_menu()
        elif choice == "4":
            self.undelete_series_menu()
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

            print(f"\n--- Books (Page {page+1}) ---")
            for idx, book in enumerate(page_books, start=1):
                # Assumes each book dictionary has at least 'id' and 'title'
                print(f"{idx}. {book['title']} (ID: {book['id']})")
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
                    else:
                        print("Invalid selection number.")
                except ValueError:
                    print("Please enter a valid number.")
            elif action == 'b':
                break
            else:
                print("Invalid option. Please try again.")

    def book_details_menu(self, book):
        """
        Displays details for the selected book and provides options to edit or delete.
        """
        print("\n==== Book Details ====")
        for key, value in book.items():
            print(f"{key}: {value}")
        print("\ne: edit, d: mark as deleted, b: back")
        choice = input("Select an option: ").strip().lower()
        if choice == 'e':
            self.edit_book_menu(book)
        elif choice == 'd':
            self.delete_book(book)
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
        new_title = input(f"Title ({book.get('title', '')}): ") or book.get('title')
        
        authors_current = ', '.join(book.get('authors', []))
        new_authors = input(f"Authors (comma separated) ({authors_current}): ")
        if new_authors:
            new_authors = [a.strip() for a in new_authors.split(',')]
        else:
            new_authors = book.get('authors', [])
        
        new_publisher = input(f"Publisher ({book.get('publisher', '')}): ") or book.get('publisher')
        new_release_year = input(f"Release Year ({book.get('release_year', '')}): ")
        new_release_year = int(new_release_year) if new_release_year else book.get('release_year')
        new_isbn_13 = input(f"ISBN 13 ({book.get('isbn_13', '')}): ") or book.get('isbn_13')
        
        tag_genre_current = ', '.join(book.get('tag_genre', []))
        new_tag_genre = input(f"Genre Tags (comma separated) ({tag_genre_current}): ")
        if new_tag_genre:
            new_tag_genre = [t.strip() for t in new_tag_genre.split(',')]
        else:
            new_tag_genre = book.get('tag_genre', [])
        
        tag_story_current = ', '.join(book.get('tag_story', []))
        new_tag_story = input(f"Story Tags (comma separated) ({tag_story_current}): ")
        if new_tag_story:
            new_tag_story = [t.strip() for t in new_tag_story.split(',')]
        else:
            new_tag_story = book.get('tag_story', [])
        
        new_description = input(f"Description ({book.get('description', '')}): ") or book.get('description')
        new_status = input(f"Status ({book.get('status', '')}): ") or book.get('status')

        updates = {
            "title": new_title,
            "authors": new_authors,
            "publisher": new_publisher,
            "release_year": new_release_year,
            "isbn_13": new_isbn_13,
            "tag_genre": new_tag_genre,
            "tag_story": new_tag_story,
            "description": new_description,
            "status": new_status,
        }
        self.db.update_book(book['id'], updates, updated_by="user")
        print("Book updated.")

    def delete_book(self, book):
        """
        Marks a book as deleted (for example by updating its status).
        """
        confirmation = input(f"Are you sure you want to mark '{book['title']}' as deleted? (y/n): ").strip().lower()
        if confirmation == 'y':
            self.db.delete_book(book['id'], updated_by="user")
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
```

### Explanation

- **Menu Structure and Routing:**  
  The `main_menu` method shows the available options. Depending on the user’s input, it calls methods for book search, series search, undelete menus, or displaying update history.

- **Pagination:**  
  Both `search_books_menu` and `undelete_book_menu` (as well as their series counterparts) display lists 10 items per page with options to navigate to the next or previous page.

- **Book and Series Operations:**  
  When a book (or series) is selected, a detailed menu lets the user view details, edit fields (with the option to leave a field unchanged), or mark the item as deleted. The deletion is assumed to update the status so that deleted items do not appear in normal searches.

- **Undelete Functionality:**  
  Separate menus (`undelete_book_menu` and `undelete_series_menu`) are provided to list deleted items and allow the user to revert the deletion (for example, by updating the status to `"active"`).

- **Update History:**  
  A simple display of the update history is provided, assuming that the database manager supplies this information.

You can run the interface (for example, in your main script) by creating an instance of your `DatabaseManager` and passing it to `DatabaseTextInterface`, then calling its `run()` method.

Adjust the implementations as needed to match your actual `DatabaseManager` methods and the structure of your book/series records.