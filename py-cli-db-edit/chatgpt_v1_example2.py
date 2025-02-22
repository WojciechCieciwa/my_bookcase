import sqlite3
import json
from datetime import datetime
import chatgpt_v1_init_and_add
import chatgpt_v1_viewer

if __name__ == "__main__":

    # Create/initialize the database (and possibly add data)
    db_manager = chatgpt_v1_init_and_add.DatabaseManager()
    db_manager.create_database("library.db")

    search_term = db_manager.prompt_search_term()

    print(search_term)
    
    results = db_manager.search_books(search_term)

    print(results)

    db_manager.close()  # Close after writing

    # Now, let's view the data
    # db_viewer = chatgpt_v1_viewer.DatabaseViewer("library.db")

    # books = db_viewer.get_all_books()
    # print("Books:", books)

    # series = db_viewer.get_all_series()
    # print("Series:", series)

    # updates = db_viewer.get_all_updates()
    # print("Updates:", updates)

    db_viewer.close()