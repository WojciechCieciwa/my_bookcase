Below is an updated example incorporating your two requested changes:

1. **Left-clicking a row** in the main listbox selects that row (and updates the highlighted selection).  
2. A **Change Table** button opens a new window listing all tables. Clicking on a table will load that table into the main window and display its first 10 rows.

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

**No major changes** from the previous version. We still use `<<DatabaseLoaded>>` to refresh the interface after a new file is loaded.

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

No changes in the menu code except for ensuring it fires `<<DatabaseLoaded>>`.

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
```

No major changes to `db_processing.py` except clarifying comments and ensuring the `current_row_index` is always in range.

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
        # 1) Left-click a row: update the current selection.
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        # 2) Double-click a row: open details in a new window.
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

        # -- Change Table button --
        self.btn_change_table = tk.Button(nav_frame, text="Change Table", command=self.change_table)
        self.btn_change_table.grid(row=0, column=10, padx=2)

    # ---------------------------------------------
    #        Main listbox handling / refresh
    # ---------------------------------------------
    def refresh_listbox(self):
        """
        Clears and reloads the listbox with the current rows.
        Also highlights the row at db_navigator.current_row_index.
        """
        self.listbox.delete(0, tk.END)
        rows_text = self.db_navigator.get_current_rows_text()
        for row in rows_text:
            self.listbox.insert(tk.END, row)

        # Highlight the currently selected row, if valid
        idx = self.db_navigator.current_row_index
        if 0 <= idx < len(rows_text):
            self.listbox.selection_set(idx)
            self.listbox.activate(idx)
            self.listbox.see(idx)

    def on_listbox_select(self, event):
        """
        Updates db_navigator.current_row_index 
        when the user left-clicks a row.
        """
        selection = self.listbox.curselection()
        if selection:
            self.db_navigator.current_row_index = selection[0]

    # ---------------------------------------------
    #        Navigation button handlers
    # ---------------------------------------------
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
        pass

    def right_arrow(self):
        pass

    # ---------------------------------------------
    #        Mouse double-click handler
    # ---------------------------------------------
    def on_double_click(self, event):
        """
        Opens a new window displaying the full content 
        of the currently selected row.
        """
        details = self.db_navigator.get_current_row_details()
        if not details:
            return
        top = tk.Toplevel(self)
        top.title("Row Details")

        txt = tk.Text(top, wrap="word")
        txt.pack(fill=tk.BOTH, expand=True)
        txt.insert(tk.END, details)

    # ---------------------------------------------
    #        Change Table functionality
    # ---------------------------------------------
    def change_table(self):
        """
        Opens a new window listing all tables in the DB.
        Clicking a table name loads that table into main UI.
        """
        top = tk.Toplevel(self)
        top.title("Select a Table")

        # Create a listbox of all tables
        lb = tk.Listbox(top, width=50, height=len(self.db_navigator.tables))
        lb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Populate the listbox with table names
        for t in self.db_navigator.tables:
            lb.insert(tk.END, t)

        # When user clicks a table (single-click), load it
        lb.bind("<<ListboxSelect>>", lambda e: self.on_table_selected(e, lb, top))

    def on_table_selected(self, event, listbox, window):
        """ 
        Loads the selected table, resets offset, 
        closes the dialog, and refreshes the main listbox.
        """
        selection = listbox.curselection()
        if not selection:
            return

        table_name = listbox.get(selection[0])
        self.db_navigator.current_table = table_name
        self.db_navigator.offset = 0
        self.db_navigator.current_row_index = 0
        self.db_navigator.load_current_rows()

        # Close the "Change Table" window
        window.destroy()

        # Refresh main listbox with the newly selected table
        self.refresh_listbox()

    # ---------------------------------------------
    #        Search functionality
    # ---------------------------------------------
    def search(self):
        text = self.search_var.get()
        self.db_navigator.search_text_in_current_table(text)
        self.refresh_listbox()
```

### Explanation of Key Changes

1. **Left-click Selection**  
   - Bound the listbox to `"<<ListboxSelect>>"` in `__init__`:  
     ```python
     self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
     ```
   - Implemented `on_listbox_select()` to set `db_navigator.current_row_index` to the newly selected row:  
     ```python
     def on_listbox_select(self, event):
         selection = self.listbox.curselection()
         if selection:
             self.db_navigator.current_row_index = selection[0]
     ```

2. **Change Table Button**  
   - Added a `Change Table` button in the navigation frame:  
     ```python
     self.btn_change_table = tk.Button(nav_frame, text="Change Table", command=self.change_table)
     self.btn_change_table.grid(row=0, column=10, padx=2)
     ```
   - `change_table()` opens a new window (`Toplevel`) containing a listbox of all table names in `db_navigator.tables`. Single-clicking a table triggers `on_table_selected()`, which sets the new `current_table`, resets pagination, and closes the dialog.  
   - Finally, it calls `refresh_listbox()` so the main UI shows the newly selected table’s rows.

With these adjustments:

- **Left-click** in the main listbox will **select** and highlight that row.  
- **Clicking "Change Table"** opens a table selector. **Click a table** to load it and update the main listbox with the first 10 rows of that table.