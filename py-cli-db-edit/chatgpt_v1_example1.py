import sqlite3
import json
from datetime import datetime
import chatgpt_v1_init_and_add
import chatgpt_v1_viewer

if __name__ == "__main__":

    # Create/initialize the database (and possibly add data)
    db_manager = chatgpt_v1_init_and_add.DatabaseManager()
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
    db_viewer = chatgpt_v1_viewer.DatabaseViewer("library.db")

    books = db_viewer.get_all_books()
    print("Books:", books)

    series = db_viewer.get_all_series()
    print("Series:", series)

    updates = db_viewer.get_all_updates()
    print("Updates:", updates)

    db_viewer.close()