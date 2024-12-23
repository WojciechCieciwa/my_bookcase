Below is an example Python project structured into the files you requested. It uses **Tkinter** for the GUI. The flow works as follows:

1. **main.py**  
   - Starts the application (creates `Tk` root).  
   - Creates the main menu (from `menu_components.py`).  
   - Creates the main UI (from `gui_components.py`).  

2. **menu_components.py**  
   - Defines a class that creates the application’s main menu (with “Open” and “Exit” options).  

3. **file_processing.py**  
   - Defines a class handling all file operations (loading text file, retrieving lines, etc.).  

4. **gui_components.py**  
   - Creates and configures GUI widgets:  
     - A listbox showing the current 10 lines.  
     - Page up/down buttons.  
     - Up/Down arrow buttons.  
     - Mouse double-click on a line to open a new window with its full content.  

Please note:
- This is a minimal, illustrative example. You can add more validation, error handling, or advanced features as needed.
- For demonstration, lines are displayed in a `Listbox`. You could alternatively use a `Text` widget or any other suitable widget.
- This sample uses a “double-click” event on the listbox item to open the top-level window. You can change that to a single-click or a button press if desired.

---

## File: **file_processing.py**

```python
class FileProcessor:
    """
    Handles file loading and basic text retrieval operations.
    """
    def __init__(self):
        self.lines = []

    def open_file(self, filename):
        """
        Opens the specified text file and reads its lines into a list.
        """
        with open(filename, 'r', encoding='utf-8') as file:
            self.lines = file.readlines()

    def get_total_lines(self):
        """
        Returns the total number of lines loaded.
        """
        return len(self.lines)

    def get_line(self, index):
        """
        Returns a single line at the specified index (empty if out of range).
        """
        if 0 <= index < len(self.lines):
            return self.lines[index]
        return ""

    def get_lines_in_range(self, start, count=10):
        """
        Returns up to `count` lines starting from `start`.
        """
        end = start + count
        return self.lines[start:end]
```

---

## File: **menu_components.py**

```python
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
```

---

## File: **gui_components.py**

```python
import tkinter as tk

class MainUI:
    """
    Builds the main interface that displays lines of text and allows navigation via page up/down, up/down arrows.
    """
    def __init__(self, root, file_processor):
        """
        :param root:           The main Tk window.
        :param file_processor: An instance of FileProcessor.
        """
        self.root = root
        self.file_processor = file_processor

        # Keep track of current start line for display and current selected index within the listbox
        self.current_start = 0
        self.selected_index = None

        # --- Create Widgets ---
        # A listbox to display lines
        self.text_box = tk.Listbox(self.root, width=50, height=10)
        self.text_box.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        # Navigation Buttons
        self.page_up_button = tk.Button(self.root, text="Page Up", command=self.page_up)
        self.page_up_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.page_down_button = tk.Button(self.root, text="Page Down", command=self.page_down)
        self.page_down_button.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.up_button = tk.Button(self.root, text="Up", command=self.move_up)
        self.up_button.grid(row=1, column=2, sticky="ew", padx=5, pady=5)

        self.down_button = tk.Button(self.root, text="Down", command=self.move_down)
        self.down_button.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

        # Bind selection event on the listbox
        self.text_box.bind('<<ListboxSelect>>', self.on_select)

        # Double-click on a line to open a new window
        self.text_box.bind("<Double-Button-1>", self.on_double_click)

    def update_display(self):
        """
        Clears and re-populates the listbox with 10 lines from the current_start index.
        """
        self.text_box.delete(0, tk.END)

        lines = self.file_processor.get_lines_in_range(self.current_start, 10)
        for line in lines:
            # Strip trailing newlines/spaces
            self.text_box.insert(tk.END, line.rstrip('\n'))

        # Reset selection index if lines changed
        self.selected_index = None

    def page_up(self):
        """
        Scrolls the view up by 10 lines (if possible), then updates the display.
        """
        self.current_start = max(0, self.current_start - 10)
        self.update_display()

    def page_down(self):
        """
        Scrolls the view down by 10 lines (if possible), then updates the display.
        """
        if self.current_start + 10 < self.file_processor.get_total_lines():
            self.current_start += 10
        self.update_display()

    def move_up(self):
        """
        Moves the highlighted row up by 1 within the current 10 lines.
        If no rows are highlighted, highlights the first displayed row.
        """
        if self.selected_index is None:
            self.selected_index = 0
        else:
            self.selected_index = max(0, self.selected_index - 1)
        self._highlight_selected()

    def move_down(self):
        """
        Moves the highlighted row down by 1 within the current 10 lines.
        If no rows are highlighted, highlights the first displayed row.
        """
        if self.selected_index is None:
            self.selected_index = 0
        else:
            # 9 is the last index if 10 lines are displayed
            self.selected_index = min(9, self.selected_index + 1)
        self._highlight_selected()

    def on_select(self, event):
        """
        When the user selects a line in the listbox, store the selection index.
        """
        widget = event.widget
        selection = widget.curselection()
        if selection:
            self.selected_index = selection[0]

    def on_double_click(self, event):
        """
        When the user double-clicks a line, open a new top-level window displaying the line's content.
        """
        if self.selected_index is not None:
            # The actual line index in the full file is current_start + selected_index
            actual_index_in_file = self.current_start + self.selected_index
            row_content = self.file_processor.get_line(actual_index_in_file)
            self._open_row_window(row_content)

    def _highlight_selected(self):
        """
        Highlights the listbox line corresponding to self.selected_index.
        """
        # Clear previous selection
        self.text_box.select_clear(0, tk.END)

        # Set new selection if the listbox has enough items
        if 0 <= self.selected_index < self.text_box.size():
            self.text_box.selection_set(self.selected_index)
            self.text_box.activate(self.selected_index)

    def _open_row_window(self, row_content):
        """
        Opens a new top-level window with the content of the selected row.
        """
        top = tk.Toplevel(self.root)
        top.title("Row Content")

        label = tk.Label(top, text=row_content, wraplength=400)
        label.pack(padx=10, pady=10)
```

---

## File: **main.py**

```python
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
```

---

### How to Run This Project

1. **Ensure all four files** (`main.py`, `menu_components.py`, `file_processing.py`, `gui_components.py`) are in the same folder.
2. **Open a terminal** in that folder.
3. **Install any dependencies** (here, standard Python installation with Tkinter is enough).
4. **Run `main.py`:**
   ```bash
   python main.py
   ```
5. **In the application**, go to **File → Open** to select a text file.  
6. The listbox will display up to 10 lines at a time. Use the navigation buttons to scroll or highlight lines. Double-click a line to open it in a new window.

This minimal example should get you started. You can extend or refine it as your requirements grow (e.g., adding a search feature, status bars, error handling, etc.). Enjoy coding!