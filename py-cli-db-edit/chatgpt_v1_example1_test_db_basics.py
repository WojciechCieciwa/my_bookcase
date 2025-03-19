import sqlite3
import json
from datetime import datetime
import chatgpt_v1_database
import chatgpt_v1_db_viewer

if __name__ == "__main__":

    # Create/initialize the database (and possibly add data)
    db_manager = chatgpt_v1_database.DatabaseManager()
    db_manager.create_database("library.db")

    # (Optional) Add sample data
    db_manager.add_book(
        authors=["Alice Anderson", "Bob the Builder"],
        title="Sample Book",
        edition="2",
        language="EN",
        location="Prague",
        publisher="Sample Publisher",
        release_year="2022",
        isbn_13="1234567890123",
        pages="133",
        tags=["Mystery", "Crime", "Detective", "Suspense"],
        description="A sample mystery book.",
        status="incomplete"
    )

    db_manager.add_book(
        authors=["Jonathan Doe", "Alicia Pardner"],
        title="Sample Book 2",
        edition="6",
        language="EN",
        location="Warsaw",
        publisher="Sample Publisher",
        release_year="2022",
        isbn_13="1236567890123",
        pages="113",
        tags=["Sci-Fi", "Novella", "Very, Very Bad", "Suspense"],
        description="A sample mystery book.",
        status="incomplete"
    )

    db_manager.add_book(
        authors=["Felix Doe"],
        title="Sample Book 3",
        edition="4",
        language="EN",
        location="New York",
        publisher="Sample Publisher",
        release_year="2023",
        isbn_13="1234567190123",
        pages="113",
        tags=["Sci-Fi", "Novella", "Very, Very Bad", "Suspense", "Another tag test"],
        description="A sample mystery book.",
        status="incomplete"
    )

    db_manager.add_series(title="Sample Series", books_ids=[1])
    db_manager.add_update(book_id=1, series_id=1, last_updated="2025-02-16", updated_by="TestUser")

    db_manager.close()  # Close after writing

    # Now, let's view the data
    db_viewer = chatgpt_v1_db_viewer.DatabaseViewer("library.db")

    books = db_viewer.get_all_books()
    print("Books: ----\n", books)

    series = db_viewer.get_all_series()
    print("Series: ----\n", series)

    updates = db_viewer.get_all_updates()
    print("Updates: ----\n", updates)

    db_viewer.close()