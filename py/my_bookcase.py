import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import os
import tempfile

# obsługa bazy danych SQLite
import sqlite3

# Global variable to store the file content or an error message.
file_content = None

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



# Tworzymy główne okno aplikacji
root = tk.Tk()
root.title("Program z rozwijalnym menu")

# Tworzymy pasek menu
menu_bar = tk.Menu(root)

# Tworzymy menu "Plik"
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Nowy", command=lambda: show_message("Nowy"))
file_menu.add_command(label="Otwórz", command=lambda: show_message("Otwórz"))
file_menu.add_command(label="Otwórz i załaduj plik do bufora", command=lambda: choose_and_load_file())
file_menu.add_command(label="Zapisz bufor na dysku", command=lambda: save_loaded_file())
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
bookcase_menu.add_command(label="Wyświetl zbuforowany plik w przeglądarce", command=lambda: display_in_browser())

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