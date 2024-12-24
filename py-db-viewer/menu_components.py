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
