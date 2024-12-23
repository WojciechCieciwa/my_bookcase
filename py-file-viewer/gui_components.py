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
