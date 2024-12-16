Below is an example of how you might structure your code into two files. The first file (`hello_world_gui.py`) defines a class that creates a main window with a "Hello World!" button. Clicking this button opens another window with "Hello World!" text. The second file (`main.py`) shows how you can use the class defined in the first file.

**File: `hello_world_gui.py`**

```python
import tkinter as tk
from tkinter import ttk

class HelloWorldApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Main Window")

        # Create a button labeled "Hello World!"
        self.button = ttk.Button(self.master, text="Hello World!", command=self.show_hello_window)
        self.button.pack(padx=20, pady=20)

    def show_hello_window(self):
        # Create a new window with the "Hello World!" text
        hello_window = tk.Toplevel(self.master)
        hello_window.title("Hello Window")

        message_label = ttk.Label(hello_window, text="Hello World!")
        message_label.pack(padx=20, pady=20)


if __name__ == "__main__":
    # This allows you to run this file directly for testing
    root = tk.Tk()
    app = HelloWorldApp(root)
    root.mainloop()
```

**File: `main.py`**

```python
import tkinter as tk
from hello_world_gui import HelloWorldApp

if __name__ == "__main__":
    root = tk.Tk()
    app = HelloWorldApp(root)
    root.mainloop()
```

**Instructions:**
1. Save the first code snippet as `hello_world_gui.py`.
2. Save the second code snippet as `main.py`.
3. Run `main.py`. This will create the main GUI window with a "Hello World!" button.
4. Click the "Hello World!" button to open the second window that displays "Hello World!".