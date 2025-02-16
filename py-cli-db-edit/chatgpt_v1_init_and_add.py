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
                release_year INTEGER,
                isbn_13 TEXT,
                tag_genre TEXT,
                tag_story TEXT,
                description TEXT,
                status TEXT
            )
        """)

        # Create 'series' table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS series (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                books TEXT
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
                 release_year: int,
                 isbn_13: str,
                 tag_genre: list,
                 tag_story: list,
                 description: str,
                 status: str):
        """
        Add a new book to the database.
        
        :param title: Title of the book
        :param authors: List of authors
        :param publisher: Publisher name
        :param release_year: Release year (integer)
        :param isbn_13: ISBN-13 identifier
        :param tag_genre: List of genre tags
        :param tag_story: List of story tags
        :param description: Description or summary of the book
        :param status: One of ['deleted','incomplete','complete','update_requested']
        """
        if not self.connection:
            raise Exception("Database not created or connected. Call create_database first.")

        authors_json = json.dumps(authors)
        tag_genre_json = json.dumps(tag_genre)
        tag_story_json = json.dumps(tag_story)

        self.cursor.execute("""
            INSERT INTO books (title, authors, publisher, release_year, isbn_13, tag_genre, tag_story, description, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, authors_json, publisher, release_year, isbn_13, tag_genre_json, tag_story_json, description, status))

        self.connection.commit()

    def add_series(self, title: str, books: list):
        """
        Add a new series to the database.
        
        :param title: Title of the series
        :param books: List of book IDs that belong to this series
        """
        if not self.connection:
            raise Exception("Database not created or connected. Call create_database first.")

        books_json = json.dumps(books)
        self.cursor.execute("""
            INSERT INTO series (title, books)
            VALUES (?, ?)
        """, (title, books_json))

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
                    tag_genre: list = None,
                    tag_story: list = None,
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

        if tag_genre is not None:
            updates.append("tag_genre = ?")
            params.append(json.dumps(tag_genre))

        if tag_story is not None:
            updates.append("tag_story = ?")
            params.append(json.dumps(tag_story))

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

    def update_series(self, series_id: int, title: str = None, books: list = None):
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

        if books is not None:
            updates.append("books = ?")
            params.append(json.dumps(books))

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
