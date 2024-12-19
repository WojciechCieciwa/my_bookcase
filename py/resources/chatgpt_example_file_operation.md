Below is an example Python program that uses `tkinter` to implement the three requested functions. For demonstration purposes, it creates a simple tkinter GUI with three buttons:

1. **Load File:**  
   Uses a hardcoded file path (for demonstration) or displays an error if it fails.
   
2. **Open in Browser:**  
   Opens the system’s default HTML browser and displays the currently loaded content (which is stored in a variable).
   
3. **Choose File and Load:**  
   Opens a file chooser dialog, lets the user pick a file, and then loads that file’s content into the variable using the first function.

### Notes on Implementation Details:

- The first function (`load_file_content`) takes a file path and tries to read its content into a variable. If it fails, it sets a global variable indicating a load error message.
  
- The second function (`display_in_browser`) uses the `webbrowser` module to open a temporary HTML file containing the variable’s content.
  
- The third function (`choose_and_load_file`) uses the `filedialog` module to present a file chooser dialog, then calls the first function to load the chosen file’s contents.

**Make sure you have read/write permission in the directory where you run the script, since a temporary HTML file will be created there.**

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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("File Loader and Browser Display")

    # Button to load a file (using a hardcoded path for demo)
    # In a real scenario, you'd choose your path or use the third function.
    load_demo_button = tk.Button(root, text="Load Demo File", command=lambda: load_file_content("example.txt"))
    load_demo_button.pack(pady=5)

    # Button to display in browser
    display_button = tk.Button(root, text="Open in Browser", command=display_in_browser)
    display_button.pack(pady=5)

    # Button to choose and load file
    choose_button = tk.Button(root, text="Choose and Load File", command=choose_and_load_file)
    choose_button.pack(pady=5)

    root.mainloop()
```

**Instructions:**

1. Make sure you have `tkinter` installed (it usually comes by default with most Python installations on Windows, macOS, and some Linux distributions).
2. Save the above code into a Python file (e.g., `app.py`).
3. Run `python app.py`.
4. Use the "Load Demo File" button after placing an `example.txt` in the same directory as the script for a quick test, or use "Choose and Load File" to pick a file from your system.
5. Click "Open in Browser" to see the loaded content displayed in your default browser.