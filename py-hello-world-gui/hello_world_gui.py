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
