Below is an example of a **separate** Python class that connects to the same SQLite database and provides methods to **retrieve/display** data from each table (i.e., `books`, `series`, and `updates`). 

In this example:

- The class constructor (`__init__`) accepts the **database filename** and creates a connection to it.
- We have three primary methods:
  - `get_all_books()`
  - `get_all_series()`
  - `get_all_updates()`
- Each method:
  1. Selects all rows from the relevant table.
  2. Deserializes any JSON fields (e.g., `authors`, `tag_genre`, `tag_story`, `books`).
  3. Returns a **list of dictionaries**, with each dictionary representing a row from the table.

You can then **print** these results in your main code or **further process** them as needed.

---

```python
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
        query = "SELECT id, title, authors, publisher, release_year, isbn_13, tag_genre, tag_story, description, status FROM books"
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
                'tag_genre': json.loads(row[6]) if row[6] else [],
                'tag_story': json.loads(row[7]) if row[7] else [],
                'description': row[8],
                'status': row[9],
            }
            books.append(book)

        return books

    def get_all_series(self):
        """
        Retrieve all series from the 'series' table.
        Returns a list of dictionaries, each dictionary containing the series data.
        JSON fields (books) are converted back into Python lists.
        """
        query = "SELECT id, title, books FROM series"
        rows = self.cursor.execute(query).fetchall()

        all_series = []
        for row in rows:
            # row = (id, title, books)
            series = {
                'id': row[0],
                'title': row[1],
                'books': json.loads(row[2]) if row[2] else []
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
```

### Example usage

Below is an example of how you might use the `DatabaseViewer` class **after** using the `DatabaseManager` (from the previous example) to insert some data.

```python
if __name__ == "__main__":
    from your_module import DatabaseManager  # Replace with your actual import

    # Create/initialize the database (and possibly add data)
    db_manager = DatabaseManager()
    db_manager.create_database("library.db")

    # (Optional) Add sample data
    db_manager.add_book(
        title="Sample Book",
        authors=["Alice", "Bob"],
        publisher="Sample Publisher",
        release_year=2022,
        isbn_13="1234567890123",
        tag_genre=["Mystery", "Crime"],
        tag_story=["Detective", "Suspense"],
        description="A sample mystery book.",
        status="incomplete"
    )
    db_manager.add_series(title="Sample Series", books=[1])
    db_manager.add_update(book_id=1, series_id=1, last_updated="2025-02-16", updated_by="TestUser")

    db_manager.close()  # Close after writing

    # Now, let's view the data
    viewer = DatabaseViewer("library.db")

    books = viewer.get_all_books()
    print("Books:", books)

    series = viewer.get_all_series()
    print("Series:", series)

    updates = viewer.get_all_updates()
    print("Updates:", updates)

    viewer.close()
```

In this example:

- **`DatabaseManager`** is used to create the database schema and perform **inserts/updates**.
- **`DatabaseViewer`** is used strictly to **retrieve and display** data from the database.

You can customize both classes (e.g., add filter conditions, pagination, or ID-based retrieval methods) as needed for your application.