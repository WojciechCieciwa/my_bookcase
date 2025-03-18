import sqlite3
import json

class DatabaseViewer:
    def __init__(self, db_name: str):
        """
        Initialize the viewer by connecting to an existing SQLite database.
        :param db_name: Path to the SQLite database file.
        """
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def get_all_books(self):
        """
        Retrieve all books from the 'books' table.
        Returns a list of dictionaries, each dictionary containing the book data.
        JSON fields (authors, tag_genre, tag_story) are converted back into Python lists.
        """
        query = "SELECT id, title, authors, publisher, release_year, isbn_13, pages, tags, description, status FROM books"
        rows = self.cursor.execute(query).fetchall()

        books = []
        for row in rows:
            # row = (id, title, authors, publisher, release_year, isbn_13, 
            #        tag_genre, tag_story, description, status)
            book = {
                'id': row[0],
                'title': row[1],
                'authors': json.loads(row[2]) if row[2] else [],
                'publisher': row[3],
                'release_year': row[4],
                'isbn_13': row[5],
                'pages': row[6],
                'tags': json.loads(row[7]) if row[7] else [],
                'description': row[7],
                'status': row[8],
            }
            books.append(book)

        return books

    def get_all_series(self):
        """
        Retrieve all series from the 'series' table.
        Returns a list of dictionaries, each dictionary containing the series data.
        JSON fields (books) are converted back into Python lists.
        """
        query = "SELECT id, title, books_ids, tags, description FROM series"
        rows = self.cursor.execute(query).fetchall()

        all_series = []
        for row in rows:
            # row = (id, title, books)
            series = {
                'id': row[0],
                'title': row[1],
                'books_ids': json.loads(row[2]) if row[2] else [],
                'tags': json.loads(row[3]) if row[3] else [],
                'description': row[4]
            }
            all_series.append(series)

        return all_series

    def get_all_updates(self):
        """
        Retrieve all update records from the 'updates' table.
        Returns a list of dictionaries, each dictionary containing the update data.
        Note: The 'last_updated' field is stored as text (e.g. 'YYYY-MM-DD') by default.
        """
        query = "SELECT id, book_id, series_id, last_updated, updated_by FROM updates"
        rows = self.cursor.execute(query).fetchall()

        updates = []
        for row in rows:
            # row = (id, book_id, series_id, last_updated, updated_by)
            update_data = {
                'id': row[0],
                'book_id': row[1],
                'series_id': row[2],
                'last_updated': row[3],
                'updated_by': row[4],
            }
            updates.append(update_data)

        return updates

    def close(self):
        """
        Close the database connection.
        """
        if self.connection:
            self.connection.close()
