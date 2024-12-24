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
