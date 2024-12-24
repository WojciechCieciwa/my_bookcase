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
