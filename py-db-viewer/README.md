Below is an updated example that meets your additional requirements:

1. **On file load**, the first **10 rows** are shown.  
2. On file load, the **first row** is automatically selected and highlighted in the listbox.  
3. The **selected line** is always highlighted.  
4. Clicking a navigation button (e.g., Up/Down/Page Up/Page Down) moves the **listbox selection** appropriately.

**Important Changes**  
- After loading a file, we generate a virtual event (`<<DatabaseLoaded>>`) so the main UI (`MainUI`) can refresh and highlight row 0.  
- In `MainUI.refresh_listbox()`, we select and highlight the row corresponding to `DBNavigator.current_row_index`.  
- Each navigation action updates `DBNavigator.current_row_index`, then calls `refresh_listbox()` to ensure selection follows.

Below are the four files with only the relevant changes highlighted.

---

## 1. **main.py**

```python
import tkinter as tk
from menu_components import MainMenu
from gui_components import MainUI
from db_processing import DatabaseHandler, DBNavigator


def main():
    root = tk.Tk()
    root.title("SQLite Viewer and Editor")

    db_handler = DatabaseHandler()
    db_navigator = DBNavigator(db_handler)

    # Create and attach the menu
    menu_bar = MainMenu(root, db_handler, db_navigator)
    root.config(menu=menu_bar)

    # Create the main UI
    main_ui = MainUI(root, db_handler, db_navigator)
    main_ui.pack(fill=tk.BOTH, expand=True)

    # When the database is loaded, refresh the UI and highlight the first row
    def on_database_loaded(event):
        main_ui.refresh_listbox()

    root.bind("<<DatabaseLoaded>>", on_database_loaded)

    root.mainloop()


if __name__ == "__main__":
    main()
```

**What’s new here?**  
- We bind a custom event `<<DatabaseLoaded>>` to a handler in the main UI. This event is generated by the menu after a file is loaded successfully.

---

## 2. **menu_components.py**

```python
import tkinter as tk
from tkinter import filedialog, messagebox


class MainMenu(tk.Menu):
    def __init__(self, parent, db_handler, db_navigator, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.db_handler = db_handler
        self.db_navigator = db_navigator

        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Save File", command=self.save_file)
        file_menu.add_command(label="Save As New File", command=self.save_as_new_file)
        self.add_cascade(label="File", menu=file_menu)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("SQLite3 Files", "*.db *.sqlite *.sqlite3"),
                ("All Files", "*.*"),
            ]
        )
        if file_path:
            try:
                self.db_handler.load_file(file_path)
                self.db_navigator.reset_navigation()
                # Generate a virtual event so the main UI knows to refresh
                self.parent.event_generate("<<DatabaseLoaded>>")
                messagebox.showinfo("Success", f"Opened: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file.\n{e}")

    def save_file(self):
        try:
            self.db_handler.save_file()
            messagebox.showinfo("Success", "File saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file.\n{e}")

    def save_as_new_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[
                ("SQLite3 Files", "*.db *.sqlite *.sqlite3"),
                ("All Files", "*.*"),
            ]
        )
        if file_path:
            try:
                self.db_handler.save_as_new_file(file_path)
                messagebox.showinfo("Success", f"Saved as new file: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save as new file.\n{e}")
```

**What’s new here?**  
- After calling `db_navigator.reset_navigation()`, we call `self.parent.event_generate("<<DatabaseLoaded>>")` so the UI refreshes and selects the first row.

---

## 3. **db_processing.py**

```python
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
            # Fallback for older SQLite versions:
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
        and self.page_size. Resets current_row_index to 0.
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
        # Make sure the current_row_index is valid
        self.current_row_index = min(self.current_row_index, len(self.current_rows) - 1)
        if self.current_row_index < 0:
            self.current_row_index = 0

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
        """
        Move the selection up by one row in the 
        currently loaded page (if possible).
        """
        if self.current_rows:
            self.current_row_index = max(0, self.current_row_index - 1)

    def move_down_one(self):
        """
        Move the selection down by one row in the
        currently loaded page (if possible).
        """
        if self.current_rows:
            self.current_row_index = min(
                len(self.current_rows) - 1, 
                self.current_row_index + 1
            )

    def move_line_start(self):
        if self.current_rows:
            self.current_row_index = 0

    def move_line_end(self):
        if self.current_rows:
            self.current_row_index = len(self.current_rows) - 1

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

        like_params = []
        where_clauses = []
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
```

**What’s new here?**  
- In `reset_navigation()`, we explicitly set `self.current_row_index = 0`.  
- After loading rows, we ensure the current_row_index doesn’t fall outside the loaded rows.  

---

## 4. **gui_components.py**

```python
import tkinter as tk
from tkinter import ttk


class MainUI(tk.Frame):
    def __init__(self, parent, db_handler, db_navigator, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.db_handler = db_handler
        self.db_navigator = db_navigator

        # -- Search area --
        self.search_var = tk.StringVar()
        search_frame = tk.Frame(self)
        search_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        tk.Label(search_frame, text="Search text:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_button = tk.Button(search_frame, text="Search", command=self.search)
        self.search_button.pack(side=tk.LEFT, padx=5)

        # -- Listbox for rows --
        self.listbox = tk.Listbox(self, width=100, height=10)
        self.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.listbox.bind("<Double-Button-1>", self.on_double_click)

        # -- Navigation buttons --
        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.TOP, pady=5)

        self.btn_file_home = tk.Button(nav_frame, text="File Home", command=self.file_home)
        self.btn_file_home.grid(row=0, column=0, padx=2)

        self.btn_file_end = tk.Button(nav_frame, text="File End", command=self.file_end)
        self.btn_file_end.grid(row=0, column=1, padx=2)

        self.btn_page_up = tk.Button(nav_frame, text="Page Up", command=self.page_up)
        self.btn_page_up.grid(row=0, column=2, padx=2)

        self.btn_page_down = tk.Button(nav_frame, text="Page Down", command=self.page_down)
        self.btn_page_down.grid(row=0, column=3, padx=2)

        self.btn_up = tk.Button(nav_frame, text="Up", command=self.move_up_one)
        self.btn_up.grid(row=0, column=4, padx=2)

        self.btn_down = tk.Button(nav_frame, text="Down", command=self.move_down_one)
        self.btn_down.grid(row=0, column=5, padx=2)

        self.btn_line_home = tk.Button(nav_frame, text="Line Home", command=self.line_home)
        self.btn_line_home.grid(row=0, column=6, padx=2)

        self.btn_line_end = tk.Button(nav_frame, text="Line End", command=self.line_end)
        self.btn_line_end.grid(row=0, column=7, padx=2)

        self.btn_left = tk.Button(nav_frame, text="Left", command=self.left_arrow)
        self.btn_left.grid(row=0, column=8, padx=2)

        self.btn_right = tk.Button(nav_frame, text="Right", command=self.right_arrow)
        self.btn_right.grid(row=0, column=9, padx=2)

    def refresh_listbox(self):
        """
        Clears and reloads the listbox with the current rows.
        Also highlights the row at db_navigator.current_row_index.
        """
        self.listbox.delete(0, tk.END)
        rows_text = self.db_navigator.get_current_rows_text()
        for row in rows_text:
            self.listbox.insert(tk.END, row)

        # Highlight the currently selected row
        idx = self.db_navigator.current_row_index
        if 0 <= idx < len(rows_text):
            self.listbox.selection_set(idx)
            self.listbox.activate(idx)
            self.listbox.see(idx)

    # ---------- Navigation button handlers ----------
    def file_home(self):
        self.db_navigator.move_first_page()
        self.refresh_listbox()

    def file_end(self):
        self.db_navigator.move_last_page()
        self.refresh_listbox()

    def page_up(self):
        self.db_navigator.page_up()
        self.refresh_listbox()

    def page_down(self):
        self.db_navigator.page_down()
        self.refresh_listbox()

    def move_up_one(self):
        self.db_navigator.move_up_one()
        self.refresh_listbox()

    def move_down_one(self):
        self.db_navigator.move_down_one()
        self.refresh_listbox()

    def line_home(self):
        self.db_navigator.move_line_start()
        self.refresh_listbox()

    def line_end(self):
        self.db_navigator.move_line_end()
        self.refresh_listbox()

    def left_arrow(self):
        # This is a placeholder in case you implement horizontal navigation
        pass

    def right_arrow(self):
        # This is a placeholder in case you implement horizontal navigation
        pass

    # ---------- Mouse double-click handler ----------
    def on_double_click(self, event):
        """
        Opens a new window displaying the full content of the currently selected row.
        """
        details = self.db_navigator.get_current_row_details()
        if not details:
            return
        top = tk.Toplevel(self)
        top.title("Row Details")

        txt = tk.Text(top, wrap="word")
        txt.pack(fill=tk.BOTH, expand=True)
        txt.insert(tk.END, details)

    # ---------- Search ----------
    def search(self):
        text = self.search_var.get()
        self.db_navigator.search_text_in_current_table(text)
        self.refresh_listbox()
```

**What’s new here?**  
- In `refresh_listbox()`, after inserting rows, we select/activate the row at `db_navigator.current_row_index`. This ensures that:  
  - On file load, row 0 is automatically selected.  
  - Whenever you move up/down a row, the highlighted selection follows.  
  - Whenever you page up/down, the highlighted selection resets to the first row in that page (or maintains `current_row_index` if so desired).

---

### How to Test

1. Place all four Python files (**main.py**, **menu_components.py**, **db_processing.py**, **gui_components.py**) in the same directory.  
2. Run `python main.py`.  
3. Click **File -> Open File** and select a valid SQLite database.  
4. You should immediately see the **first 10 rows** in the listbox, with **row 0 highlighted**.  
5. Press **Down** to move selection down, **Up** to move it up, etc. The selection in the listbox should follow the currently highlighted row.