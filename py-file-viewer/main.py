import tkinter as tk
from menu_components import AppMenu
from file_processing import FileProcessor
from gui_components import MainUI

def main():
    root = tk.Tk()
    root.title("Text File Viewer")

    # Create a FileProcessor instance
    file_processor = FileProcessor()

    # Create the main UI. We will pass a callback into the menu so that
    # once a file is opened, the main UI display can be refreshed.
    main_ui = MainUI(root, file_processor)

    def update_display():
        """
        Callback function used by the menu after loading a file.
        Tells the main UI to refresh.
        """
        main_ui.current_start = 0  # Reset to display from the first line again
        main_ui.update_display()

    # Create menu bar
    AppMenu(root, file_processor, update_display)

    root.mainloop()

if __name__ == "__main__":
    main()
