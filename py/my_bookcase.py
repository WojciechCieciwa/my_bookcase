import tkinter as tk
from tkinter import messagebox

# obsługa bazy danych SQLite
import sqlite3

# obsługa ISBN

# obsługa kodów kreskowych

# obsługa baz książek

# Funkcja dla opcji w menu
def show_message(option):
    messagebox.showinfo("Wybór", f"Wybrano opcję: {option}")

# Funkcja definiująca tekst informujący o programie
def show_about_program(option):
    messagebox.showinfo("O Programie...", f"Program 'Moja biblioteczka' pozwala ogarnąć zarządzanie swoim księgozbiorem. {option}")

# tekst informujacy o stanie pliku bazy z ksiazkami
def show_libraryfileinfo(option):
    messagebox.showinfo("Informacja o bazie danych","XYZ")

# Tworzymy główne okno aplikacji
root = tk.Tk()
root.title("Program z rozwijalnym menu")

# Tworzymy pasek menu
menu_bar = tk.Menu(root)

# Tworzymy menu "Plik"
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Nowy", command=lambda: show_message("Nowy"))
file_menu.add_command(label="Otwórz", command=lambda: show_message("Otwórz"))
file_menu.add_separator()  # Dodanie separatora
file_menu.add_command(label="Zakończ", command=root.quit)

# Tworzymy menu "Edycja"
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Kopiuj", command=lambda: show_message("Kopiuj"))
edit_menu.add_command(label="Wklej", command=lambda: show_message("Wklej"))

# Tworzymy menu "Biblioteczka"
bookcase_menu = tk.Menu(menu_bar, tearoff=0)
bookcase_menu.add_command(label="Analizuj...", command=lambda: show_libraryfileinfo(""))
bookcase_menu.add_separator() # dodanie separatora

# Tworzymy menu "Pomoc"
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Pomoc", command=lambda: show_message("Pomoc") )
help_menu.add_separator() # dodanie separatora
help_menu.add_command(label="O Programie", command=lambda: show_about_program(""))

# Dodanie menu do paska menu
menu_bar.add_cascade(label="Plik", menu=file_menu)
menu_bar.add_cascade(label="Edycja", menu=edit_menu)
menu_bar.add_cascade(label="Bookcase", menu=bookcase_menu)
menu_bar.add_cascade(label="Pomoc", menu=help_menu)


# start programu
# sprawdzanie obecności pliku konfiguracyjnego
# jeśli jest wczytanie wartości
# niema przyjmujemy [w zależności od systemu operacyjnego]:
# dla PC
## wielkość okna: 640x480
root.geometry("800x600")

root.minsize(640, 480)

root.maxsize(1024, 768)

## katalog konfiguracyjny: ~/appdata/local/bookcase
## katalog roboczy: ~/temp
# inne jeszcze nie zrobione
 
# jeśli był parametr (traktowany jako nazwa bazy) sprawdzamy czy jest w ~/Documents/My Bookcase/ plik o nazwie "parametr"
## jeśli jest sprawdzamy czy jest to plik SQLite'a
### TAK - wczytujemy strukturę
### NIE - komunikat o błędzie i informacja, że jest prawdopodobnie uszkodzony plik i propozycja założenia nowej bazy pod nazwą "parametr"_new.sql
## jeśli nie było pliku zakładamy nową bazę o domyślnej strukturze (-> struktura bazy)

##### tymczasowe
mylib_con = sqlite3.connect("mylibrary.db")
mylib_cur = mylib_con.cursor()

# Ustawienie paska menu w oknie głównym
root.config(menu=menu_bar)

# Uruchomienie głównej pętli aplikacji
root.mainloop()