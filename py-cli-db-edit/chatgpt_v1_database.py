import sqlite3
import json
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        """
        The constructor doesn't initialize or connect to any database by default.
        Call create_database(db_name) to create/connect to a SQLite database.
        """
        self.connection = None
        self.cursor = None

    def create_database(self, db_name: str):
        """
        Create (or connect to) a SQLite database file with the given name
        and create the necessary tables if they do not exist.
        
        :param db_name: The name (or path) of the SQLite database file.
        """
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

        # Create 'books' table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                authors TEXT,
                publisher TEXT,
                release_year TEXT,
                isbn_13 TEXT NOT NULL,
                pages TEXT,
                tags TEXT,
                description TEXT,
                status TEXT
            )
        """)

        # Create 'series' table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS series (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                books_ids TEXT,
                tags TEXT,
                description TEXT
            )
        """)

        # Create 'updates' table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                series_id INTEGER,
                last_updated TEXT,
                updated_by TEXT,
                FOREIGN KEY(book_id) REFERENCES books(id),
                FOREIGN KEY(series_id) REFERENCES series(id)
            )
        """)

        self.connection.commit()

    def add_book(self,
                 title: str,
                 authors: list,
                 publisher: str,
                 release_year: str,
                 isbn_13: str,
                 pages: str,
                 tags: list,
                 description: str,
                 status: str):
        """
        Add a new book to the database.
        
        :param title: Title of the book
        :param authors: List of authors
        :param publisher: Publisher name
        :param release_year: Release year (integer)
        :param isbn_13: ISBN-13 identifier
        :param pages: Number of pages
        :param tags: List of tags
        :param description: Description or summary of the book
        :param status: One of ['deleted','incomplete','complete','update_requested']
        """
        if not self.connection:
            raise Exception("Database not created or connected. Call create_database first.")

        authors_json = json.dumps(authors)
        tags_json = json.dumps(tags)

        # dodajemy blokade duplikatu ISBN

        query = "SELECT isbn_13 FROM books WHERE isbn_13 = '" + str(isbn_13) + "'"
        self.cursor.execute(query)
        rows = self.cursor.execute(query).fetchall()
        if rows:
            return False

        self.cursor.execute("""
            INSERT INTO books (title, authors, publisher, release_year, isbn_13, pages, tags, description, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, authors_json, publisher, release_year, isbn_13, pages, tags_json, description, status))

        self.connection.commit()
        return True

    def add_series(self, title: str, books_ids: list = [], tags: list = [], description: str = None):
        """
        Add a new series to the database.
        
        :param title: Title of the series
        :param books: List of book IDs that belong to this series
        """
        if not self.connection:
            raise Exception("Database not created or connected. Call create_database first.")

        books_json = json.dumps(books_ids)
        tags_json = json.dumps(tags)

        self.cursor.execute("""
            INSERT INTO series (title, books_ids, tags, description)
            VALUES (?, ?, ?, ?)
        """, (title, books_json, tags_json, description))

        self.connection.commit()

    def add_update(self, book_id: int, series_id: int, last_updated: str, updated_by: str):
        """
        Add a new update record to the database.
        
        :param book_id: The ID of the associated book (can be None if not related to a specific book)
        :param series_id: The ID of the associated series (can be None if not related to a specific series)
        :param last_updated: Date as string in format YYYY-MM-DD (or other format as desired)
        :param updated_by: Person or process that made the update
        """
        if not self.connection:
            raise Exception("Database not created or connected. Call create_database first.")

        self.cursor.execute("""
            INSERT INTO updates (book_id, series_id, last_updated, updated_by)
            VALUES (?, ?, ?, ?)
        """, (book_id, series_id, last_updated, updated_by))

        self.connection.commit()

    def update_book(self,
                    book_id: int,
                    title: str = None,
                    authors: list = None,
                    publisher: str = None,
                    release_year: int = None,
                    isbn_13: str = None,
                    pages: str = None,
                    tags: list = None,
                    description: str = None,
                    status: str = None):
        """
        Update fields for an existing book by its ID.
        Only non-None parameters will be updated.
        
        :param book_id: The ID of the book to update
        :param title: New title (optional)
        :param authors: New list of authors (optional)
        :param publisher: New publisher name (optional)
        :param release_year: New release year (optional)
        :param isbn_13: New ISBN-13 (optional)
        :param tag_genre: New list of genre tags (optional)
        :param tag_story: New list of story tags (optional)
        :param description: New description (optional)
        :param status: New status (optional)
        """
        if not self.connection:
            raise Exception("Database not created or connected. Call create_database first.")

        # Gather the fields to update
        updates = []
        params = []

        if title is not None:
            updates.append("title = ?")
            params.append(title)

        if authors is not None:
            updates.append("authors = ?")
            params.append(json.dumps(authors))

        if publisher is not None:
            updates.append("publisher = ?")
            params.append(publisher)

        if release_year is not None:
            updates.append("release_year = ?")
            params.append(release_year)

        if isbn_13 is not None:
            updates.append("isbn_13 = ?")
            params.append(isbn_13)

        if tags is not None:
            updates.append("tags = ?")
            params.append(json.dumps(tags))

        if pages is not None:
            updates.append("pages = ?")
            params.append(str(pages))

        if description is not None:
            updates.append("description = ?")
            params.append(description)

        if status is not None:
            updates.append("status = ?")
            params.append(status)

        # Construct the SQL update query dynamically
        if updates:
            query = "UPDATE books SET " + ", ".join(updates) + " WHERE id = ?"
            params.append(book_id)
            self.cursor.execute(query, params)
            self.connection.commit()

    def update_series(self, 
        series_id: int, 
        title: str = None, 
        books_ids: list = None, 
        tags: list = None, 
        description: str = None):
        """
        Update fields for an existing series by its ID.
        Only non-None parameters will be updated.
        
        :param series_id: The ID of the series to update
        :param title: New title (optional)
        :param books: New list of book IDs (optional)
        """
        if not self.connection:
            raise Exception("Database not created or connected. Call create_database first.")

        updates = []
        params = []

        if title is not None:
            updates.append("title = ?")
            params.append(title)

        if books_ids is not None:
            updates.append("books_ids = ?")
            params.append(json.dumps(books_ids))

        if tags is not None:
            updates.append("tags = ?")
            params.append(json.dumps(tags))

        if description is not None:
            updates.append("description = ?")
            params.append(description)

        if updates:
            query = "UPDATE series SET " + ", ".join(updates) + " WHERE id = ?"
            params.append(series_id)
            self.cursor.execute(query, params)
            self.connection.commit()

    def update_update(self, update_id: int,
                      book_id: int = None,
                      series_id: int = None,
                      last_updated: str = None,
                      updated_by: str = None):
        """
        Update fields for an existing update entry by its ID.
        Only non-None parameters will be updated.
        
        :param update_id: The ID of the update record to change
        :param book_id: New book ID (optional)
        :param series_id: New series ID (optional)
        :param last_updated: New date as string (optional)
        :param updated_by: New updated_by name/identifier (optional)
        """
        if not self.connection:
            raise Exception("Database not created or connected. Call create_database first.")

        updates = []
        params = []

        if book_id is not None:
            updates.append("book_id = ?")
            params.append(book_id)

        if series_id is not None:
            updates.append("series_id = ?")
            params.append(series_id)

        if last_updated is not None:
            updates.append("last_updated = ?")
            params.append(last_updated)

        if updated_by is not None:
            updates.append("updated_by = ?")
            params.append(updated_by)

        if updates:
            query = "UPDATE updates SET " + ", ".join(updates) + " WHERE id = ?"
            params.append(update_id)
            self.cursor.execute(query, params)
            self.connection.commit()

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def _get_connection(self):
        """
        Returns a new connection to the SQLite database.
        """
        # return sqlite3.connect(self.db_path)
        self.create_database("library.db")
        if not self.connection:
            raise Exception("Database not created or connected. Call create_database first.")
        return self.connection


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
            pages,
            tags,
            description,
            status
        FROM books
        WHERE title LIKE ?
           OR authors LIKE ?
           OR isbn_13 LIKE ?
           OR publisher LIKE ?
           OR tags LIKE ?
           OR release_year LIKE ?
           OR description LIKE ?
        """

        like_term = f"%{search_term}%"
        params = (like_term, like_term, like_term, like_term, like_term, like_term, like_term)

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


# Example usage:
if __name__ == "__main__":
    db = DatabaseManager()
    db.create_database("library.db")

    # Add a book
    db.add_book(
        title="Example Book",
        authors=["John Doe", "Jane Smith"],
        publisher="Example Publisher",
        release_year=2021,
        isbn_13="1234567890123",
        tag_genre=["Fiction", "Adventure"],
        tag_story=["Epic", "Fantasy"],
        description="An example book description.",
        status="incomplete"
    )

    # Add a series
    db.add_series(
        title="Example Series",
        books=[1]  # Suppose the book we just added has id=1
    )

    # Add an update
    db.add_update(
        book_id=1,
        series_id=1,
        last_updated="2025-02-16",
        updated_by="Admin"
    )

    # Update the book
    db.update_book(
        book_id=1,
        status="complete",
        release_year=2022
    )

    # Update the series
    db.update_series(
        series_id=1,
        books=[1, 2]  # Suppose there's a second book
    )

    # Update the update record
    db.update_update(
        update_id=1,
        updated_by="UpdaterBot"
    )

    db.close()
