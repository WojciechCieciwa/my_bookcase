Below is an updated version of the previous code that includes one more function to save the currently loaded file content to a new file on disk. This new function:

- Opens a "Save As" dialog to let the user choose where to save the file.
- If valid content is loaded, it writes this content to the new file.
- If no valid content is loaded, it displays an error message.

```python
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import os
import tempfile

# Global variable to store the file content or an error message.
file_content = None

def load_file_content(file_path):
    """
    Tries to load text file content into file_content variable.
    If unsuccessful, sets file_content to an error message.
    """
    global file_content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
    except Exception as e:
        file_content = f"Error: Could not load file. {str(e)}"

def display_in_browser():
    """
    Opens the system’s default HTML browser and displays the current file_content.
    If file_content is None or an error message, it shows a tkinter messagebox.
    Otherwise, it writes the content to a temporary HTML file and opens it.
    """
    global file_content
    
    if file_content is None or file_content.startswith("Error:"):
        messagebox.showerror("Error", "No valid content loaded to display.")
        return

    # Create a temporary HTML file and write the content into it.
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as temp_file:
        temp_file.write(file_content)
        temp_file_path = temp_file.name

    # Open the temporary file in the default browser
    webbrowser.open_new_tab(temp_file_path)

def choose_and_load_file():
    """
    Opens a file chooser dialog, allows the user to pick a file,
    and then uses load_file_content() to load it.
    """
    file_path = filedialog.askopenfilename(
        title="Choose a text file",
        filetypes=[("Text files", "*.txt;*.html;*.htm;*.md;*.py;*.log;*.csv;*.json"), ("All files", "*.*")]
    )
    if file_path:
        load_file_content(file_path)
        if file_content and not file_content.startswith("Error:"):
            messagebox.showinfo("Success", f"File loaded: {file_path}")
        else:
            messagebox.showerror("Error", "Failed to load the selected file.")

def save_loaded_file():
    """
    Saves the currently loaded content to a new file.
    If no valid content is loaded, shows an error message.
    """
    global file_content
    if file_content is None or file_content.startswith("Error:"):
        messagebox.showerror("Error", "No valid content available to save.")
        return
    
    # Ask user for a save location
    save_path = filedialog.asksaveasfilename(
        title="Save File As",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt;*.html;*.htm;*.md;*.py;*.log;*.csv;*.json"), ("All files", "*.*")]
    )
    if save_path:
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            messagebox.showinfo("Success", f"File saved to: {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file. {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("File Loader and Browser Display")

    # Button to load a file (using a hardcoded path for demo)
    load_demo_button = tk.Button(root, text="Load Demo File", command=lambda: load_file_content("example.txt"))
    load_demo_button.pack(pady=5)

    # Button to display in browser
    display_button = tk.Button(root, text="Open in Browser", command=display_in_browser)
    display_button.pack(pady=5)

    # Button to choose and load file
    choose_button = tk.Button(root, text="Choose and Load File", command=choose_and_load_file)
    choose_button.pack(pady=5)

    # Button to save the loaded file
    save_button = tk.Button(root, text="Save Loaded File", command=save_loaded_file)
    save_button.pack(pady=5)

    root.mainloop()
```

**Instructions:**

1. Ensure `tkinter` is installed and working.
2. Save the code into a Python file, e.g., `app.py`.
3. Run `python app.py`.
4. Load a file either by using "Choose and Load File" or by ensuring `example.txt` exists and using "Load Demo File".
5. Once loaded, you can display it in a browser, and also use "Save Loaded File" to save it to a new location.