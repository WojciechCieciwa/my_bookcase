import tkinter as tk
from tkinter import filedialog

class AppMenu:
    """
    Defines the application menu bar, with an 'Open' command and an 'Exit' command.
    """
    def __init__(self, root, file_processor, update_display_callback):
        """
        :param root:               The main Tk window.
        :param file_processor:     An instance of FileProcessor.
        :param update_display_callback: A callback function to refresh the main UI after a file is opened.
        """
        self.root = root
        self.file_processor = file_processor
        self.update_display_callback = update_display_callback

        # Create a top-level menubar
        menubar = tk.Menu(self.root)

        # 'File' menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Attach the menubar to the root window
        self.root.config(menu=menubar)

    def open_file(self):
        """
        Opens a file dialog for the user to select a .txt file, then updates the display.
        """
        filename = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filename:
            self.file_processor.open_file(filename)
            self.update_display_callback()
