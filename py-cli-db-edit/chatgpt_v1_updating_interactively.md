Below is an example `DatabaseManager` class in Python that illustrates the flow you requested:  

1. Prompt the user for a search string.  
2. Search for partial matches in the **books** table.  
3. Prompt the user to edit fields (or delete the book).  
4. Display changes, confirm, then update the book and record an entry in the **updates** table.  

```python
import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path):
        """
        Initialize the DatabaseManager with the path to the SQLite database.
        """
        self.db_path = db_path

    def _get_connection(self):
        """
        Returns a new connection to the SQLite database.
        """
        return sqlite3.connect(self.db_path)

    def prompt_search_term(self):
        """
        Prompt the user to enter a search string and return it.
        """
        return input("Enter a search term: ").strip()

    def search_books(self, search_term):
        """
        Searches the books table for partially matching strings in
        title, authors, isbn_13, publisher, release_year, and description.

        Returns a list of matching book records (as tuples or dicts).
        """
        query = """
        SELECT
            id,
            title,
            authors,
            publisher,
            release_year,
            isbn_13,
            tag_genre,
            tag_story,
            description,
            status
        FROM books
        WHERE title LIKE ?
           OR authors LIKE ?
           OR isbn_13 LIKE ?
           OR publisher LIKE ?
           OR CAST(release_year AS TEXT) LIKE ?
           OR description LIKE ?
        """

        like_term = f"%{search_term}%"
        params = (like_term, like_term, like_term, like_term, like_term, like_term)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()

        return results

    def prompt_book_selection(self, books):
        """
        Given a list of book rows, display them to the user and let them select one by ID.
        Returns the selected book's row (tuple) or None if invalid selection.
        """
        if not books:
            print("No books found.")
            return None

        print("\nSearch results:")
        for book in books:
            (book_id, title, authors, publisher, release_year,
             isbn_13, tag_genre, tag_story, description, status) = book
            print(f"[ID: {book_id}] {title} by {authors} (ISBN: {isbn_13})")

        while True:
            try:
                choice = input("\nEnter the ID of the book you want to edit (or 'q' to quit): ").strip()
                if choice.lower() == 'q':
                    return None
                choice_id = int(choice)
                selected = next((b for b in books if b[0] == choice_id), None)
                if selected:
                    return selected
                else:
                    print("Invalid ID. Please try again.")
            except ValueError:
                print("Please enter a valid ID or 'q' to quit.")

    def prompt_book_edit(self, book):
        """
        Prompt the user to edit any of the book fields except the book ID. 
        Also allow the user to delete the book.
        
        Returns:
            - A dictionary of updated fields if editing.
            - A special indicator (e.g., {"delete": True}) if user chooses to delete.
            - None if the user chooses to cancel.
        """
        (book_id, title, authors, publisher, release_year,
         isbn_13, tag_genre, tag_story, description, status) = book

        print("\nCurrent book details:")
        print(f"ID: {book_id}")
        print(f"1) Title: {title}")
        print(f"2) Authors: {authors}")
        print(f"3) Publisher: {publisher}")
        print(f"4) Release Year: {release_year}")
        print(f"5) ISBN-13: {isbn_13}")
        print(f"6) tag_genre: {tag_genre}")
        print(f"7) tag_story: {tag_story}")
        print(f"8) Description: {description}")
        print(f"9) Status: {status}")

        print("\nChoose a field to edit (1-9). Type 'd' to delete the book, or 'q' to cancel.")
        updates = {}

        while True:
            choice = input("Enter your choice (or press Enter when done): ").strip().lower()
            if choice == '':
                # User pressed Enter with no choice -> Done editing
                break

            if choice == 'q':
                # Cancel
                return None

            if choice == 'd':
                confirm_delete = input("Are you sure you want to delete this book? (y/n): ").strip().lower()
                if confirm_delete == 'y':
                    return {"delete": True}
                else:
                    continue

            # Map choice to a field name:
            field_map = {
                '1': ("title", title),
                '2': ("authors", authors),
                '3': ("publisher", publisher),
                '4': ("release_year", release_year),
                '5': ("isbn_13", isbn_13),
                '6': ("tag_genre", tag_genre),
                '7': ("tag_story", tag_story),
                '8': ("description", description),
                '9': ("status", status),
            }

            if choice in field_map:
                field_name, old_value = field_map[choice]
                new_value = input(f"Enter new value for {field_name} (current: {old_value}): ")
                # Convert release_year to int if user actually gave a numeric input
                if field_name == 'release_year':
                    try:
                        new_value = int(new_value)
                    except ValueError:
                        print("Invalid year. Keeping old value.")
                        continue

                updates[field_name] = new_value
            else:
                print("Invalid choice. Please try again.")

        return updates

    def display_changes_and_confirm(self, book_id, current_data, updates):
        """
        Display the proposed changes to the user and ask for confirmation.
        Returns True if the user confirms, False otherwise.
        """
        print("\nYou are about to update the following fields for book ID:", book_id)
        for field, new_value in updates.items():
            old_value = current_data.get(field, "(unknown)")
            print(f" - {field}: '{old_value}' -> '{new_value}'")

        confirm = input("\nConfirm updates? (y/n): ").strip().lower()
        return (confirm == 'y')

    def update_book(self, book_id, updates, updated_by="script"):
        """
        Update the book record in the books table and record the update in the updates table.
        """
        # 1) Update the books table
        set_clause = ", ".join(f"{field} = ?" for field in updates.keys())
        values = list(updates.values())
        values.append(book_id)  # for the WHERE clause

        update_query = f"UPDATE books SET {set_clause} WHERE id = ?"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(update_query, values)

            # 2) Record an update in the updates table
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updates_insert_query = """
                INSERT INTO updates (book_id, series_id, last_updated, updated_by)
                VALUES (?, ?, ?, ?)
            """
            # For this example, we'll pass series_id as None (or 0 if you prefer).
            cursor.execute(updates_insert_query, (book_id, None, now_str, updated_by))
            conn.commit()

    def delete_book(self, book_id, updated_by="script"):
        """
        Delete the specified book from the books table and record the update in the updates table.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # 1) Delete from books table
            delete_query = "DELETE FROM books WHERE id = ?"
            cursor.execute(delete_query, (book_id,))

            # 2) Record the 'update' in the updates table
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updates_insert_query = """
                INSERT INTO updates (book_id, series_id, last_updated, updated_by)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(updates_insert_query, (book_id, None, now_str, updated_by))
            conn.commit()

    def _get_book_as_dict(self, book_tuple):
        """
        Utility method to convert a book tuple into a dictionary for easier old/new comparison.
        """
        (book_id, title, authors, publisher, release_year,
         isbn_13, tag_genre, tag_story, description, status) = book_tuple

        return {
            "id": book_id,
            "title": title,
            "authors": authors,
            "publisher": publisher,
            "release_year": release_year,
            "isbn_13": isbn_13,
            "tag_genre": tag_genre,
            "tag_story": tag_story,
            "description": description,
            "status": status
        }

    def run(self):
        """
        Main workflow:
          1. Prompt for a search term
          2. Search for matching books
          3. Prompt user to select a book
          4. Prompt user to edit or delete
          5. Show changes, confirm, then update or delete
        """
        search_term = self.prompt_search_term()
        results = self.search_books(search_term)

        selected_book = self.prompt_book_selection(results)
        if not selected_book:
            # Either 'q' or no valid selection
            return

        # Prompt user for edits (or delete)
        edit_data = self.prompt_book_edit(selected_book)
        if edit_data is None:
            print("No changes made.")
            return

        # If user chose to delete
        if "delete" in edit_data and edit_data["delete"]:
            self.delete_book(selected_book[0])  # first element is book_id
            print(f"Book ID {selected_book[0]} has been deleted.")
            return

        # Otherwise, user is updating fields
        # selected_book is a tuple; let's turn it into a dict for old values
        current_data = self._get_book_as_dict(selected_book)

        if not edit_data:
            print("No fields were updated.")
            return

        # Show changes and confirm
        if self.display_changes_and_confirm(selected_book[0], current_data, edit_data):
            self.update_book(selected_book[0], edit_data)
            print("Book updated successfully.")
        else:
            print("Update canceled.")


if __name__ == "__main__":
    # Example usage:
    # 1) Initialize with your DB path
    db_manager = DatabaseManager("my_library.db")
    # 2) Run the main workflow
    db_manager.run()
```

### How this works:

1. **`prompt_search_term()`**  
   - Asks the user to type in a search term (string).

2. **`search_books(search_term)`**  
   - Searches the **books** table for any row where any of these columns match the search term (using `LIKE` with wildcards):  
     - `title`, `authors`, `isbn_13`, `publisher`, `release_year`, `description`.  
   - Returns a list of rows found.

3. **`prompt_book_selection(books)`**  
   - Displays the found books and asks the user to pick a book by **ID**.  
   - Returns the selected row as a tuple.

4. **`prompt_book_edit(book)`**  
   - Displays the details of the selected book.  
   - Asks the user to choose which field to edit (1–9), or optionally delete the book (`d`).  
   - Builds and returns a dictionary of field updates, e.g. `{"title": "New Title", "authors": "New Author"}`.  
   - If the user chooses to delete, returns `{"delete": True}`.  
   - If the user cancels, returns `None`.

5. **`display_changes_and_confirm(book_id, current_data, updates)`**  
   - Shows the user what changes will be made and asks them to confirm with a `(y/n)` prompt.  
   - Returns `True` if the user confirms, else `False`.

6. **`update_book(book_id, updates, updated_by="script")`**  
   - Updates the **books** table with the new field values.  
   - Inserts a row into the **updates** table containing the `book_id`, a `series_id` (set to `None` in the example), the timestamp, and the name of the user making the update (`updated_by`).

7. **`delete_book(book_id, updated_by="script")`**  
   - Deletes the book row from the **books** table.  
   - Inserts a row into the **updates** table (so you have a record of who/when the book was removed).

8. **`run()`**  
   - Orchestrates the entire flow: prompt → search → select → edit/delete → confirm → update.

You can modify `updated_by` to capture the actual user's name instead of `"script"`. You can also adjust the logic if you prefer a different flow or more refined user interaction.