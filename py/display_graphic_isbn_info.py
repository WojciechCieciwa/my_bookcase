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
book_data_text = ""
#book_data_text = ("\n"+book_data["title"]+"\n"+book_data["authors"])
#przygotować:
# na poczatek pusty string
# potem w petli
# book_data_text ma byc suma poszczegolnych pol
# gdzie są wymienione wszystkie pola (klucze tych pol) nawet jesli pole jest puste
# na koniec book_data_text jest prezentowane w okienku.
show_message(book_data_text)
