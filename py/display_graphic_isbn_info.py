import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import os
import tempfile

import isbn_info

#def get_book_info2(isbn):

#print(isbn_info.get_book_info2("9781556341274")) ## for test

def show_message(option):
    messagebox.showinfo(" ",f"{option}")

book_data = isbn_info.get_book_info2("9781556341274")
#book_data_text = "\n".join(book_data.values())
book_data_text = "\n".join(book_data["title"])
show_message(book_data_text)
