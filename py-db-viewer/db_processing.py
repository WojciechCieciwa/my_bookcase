import sqlite3
import shutil


class DatabaseHandler:
    """
    Handles basic DB operations: loading, saving, 
    and saving to a new SQLite database file.
    """
    def __init__(self):
        self.connection = None
        self.file_path = None

    def load_file(self, file_path):
        """Loads a new SQLite file, closing the current one if necessary."""
        if self.connection:
            self.connection.close()
        self.connection = sqlite3.connect(file_path)
        self.file_path = file_path

    def save_file(self):
        """
        Saves changes to the current database file.
        """
        if not self.connection or not self.file_path:
            raise Exception("No file is loaded. Cannot save.")
        self.connection.commit()

    def save_as_new_file(self, new_file_path):
        """Saves the current database to a new file."""
        if not self.connection or not self.file_path:
            raise Exception("No file is loaded. Cannot save as new file.")

        self.connection.commit()
        try:
            self.connection.execute(f"VACUUM INTO '{new_file_path}'")
        except sqlite3.OperationalError:
            self.connection.close()
            shutil.copy(self.file_path, new_file_path)
            self.connection = sqlite3.connect(self.file_path)


class DBNavigator:
    """
    Handles navigation, viewing, and (optionally) editing 
    of the loaded SQLite file's rows.
    """
    def __init__(self, db_handler):
        self.db_handler = db_handler
        self.current_table = None
        self.tables = []
        self.current_rows = []
        self.current_row_index = 0
        self.page_size = 10
        self.offset = 0

    def reset_navigation(self):
        """
        Clears current navigation state, refreshes
        the table list, and loads the first table (if any).
        """
        conn = self.db_handler.connection
        if not conn:
            return

        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        self.tables = [row[0] for row in cursor.fetchall()]

        self.current_table = self.tables[0] if self.tables else None
        self.offset = 0
        self.current_row_index = 0
        self.load_current_rows()

    def load_current_rows(self):
        """
        Loads rows for the current table, using self.offset
        and self.page_size. Resets current_row_index if needed.
        """
        self.current_rows = []
        if not self.current_table:
            return

        conn = self.db_handler.connection
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM {self.current_table} "
            f"LIMIT {self.page_size} OFFSET {self.offset}"
        )
        self.current_rows = cursor.fetchall()
        # Adjust current_row_index if out of range
        self.current_row_index = min(self.current_row_index, len(self.current_rows) - 1)
        if self.current_row_index < 0:
            self.current_row_index = 0

    # ------------ Navigation methods ------------
    def move_first_page(self):
        self.offset = 0
        self.load_current_rows()

    def move_last_page(self):
        if not self.current_table:
            return
        conn = self.db_handler.connection
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.current_table}")
        total_rows = cursor.fetchone()[0]
        if total_rows > 0:
            self.offset = ((total_rows - 1) // self.page_size) * self.page_size
        else:
            self.offset = 0
        self.load_current_rows()

    def page_up(self):
        self.offset = max(0, self.offset - self.page_size)
        self.load_current_rows()

    def page_down(self):
        self.offset += self.page_size
        self.load_current_rows()

    def move_up_one(self):
        if self.current_rows:
            self.current_row_index = max(0, self.current_row_index - 1)

    def move_down_one(self):
        if self.current_rows:
            self.current_row_index = min(len(self.current_rows) - 1,
                                         self.current_row_index + 1)

    def move_line_start(self):
        if self.current_rows:
            self.current_row_index = 0

    def move_line_end(self):
        if self.current_rows:
            self.current_row_index = len(self.current_rows) - 1

    # ------------ Data retrieval methods ------------
    def get_current_rows_text(self):
        """Return string representations of the current page's rows."""
        return [str(row) for row in self.current_rows]

    def get_current_row_details(self):
        """Return a detailed string for the currently selected row."""
        if self.current_rows and 0 <= self.current_row_index < len(self.current_rows):
            return str(self.current_rows[self.current_row_index])
        return ""

    def search_text_in_current_table(self, text):
        if not self.current_table:
            return

        conn = self.db_handler.connection
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({self.current_table})")
        columns = [col[1] for col in cursor.fetchall()]
        if not columns:
            return

        where_clauses = []
        like_params = []
        for col in columns:
            where_clauses.append(f"{col} LIKE ?")
            like_params.append(f"%{text}%")

        query = (
            f"SELECT * FROM {self.current_table} "
            f"WHERE {' OR '.join(where_clauses)} "
            f"LIMIT {self.page_size} OFFSET 0"
        )
        cursor.execute(query, tuple(like_params))
        self.current_rows = cursor.fetchall()
        self.offset = 0
        self.current_row_index = 0
