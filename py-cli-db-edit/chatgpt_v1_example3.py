import sqlite3
import json
from datetime import datetime
import chatgpt_v1_init_and_add
import chatgpt_v1_viewer
import chatgpt_v1_text_interface

if __name__ == "__main__":

    # Create/initialize the database (and possibly add data)
    db_manager = chatgpt_v1_init_and_add.DatabaseManager()
    db_manager.create_database("library.db")

    text_ui = chatgpt_v1_text_interface.DatabaseTextInterface(db_manager)

    text_ui.run()