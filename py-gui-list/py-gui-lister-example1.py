from tkinter import *

root = Tk()

# tytul okna - bazowo nazwa programu, potem albo nazwa pliku z biblioteką, albo tytuł otwartej pozycji (albo ISBN)
root.title("Tytuł okna - kiedyś będzie inny")

# startowa wielkosc interfejsu bazowo SVGA
root.geometry("1024x768")

# tworzymy obszar roboczy aplikacji
app = Frame(root)

# a tu nie mam pojecie co i jak i dlaczego ? - ale tak stoi w książce to pewnie tak być powinno bo nie jest to wyjaśnione

app.grid()

# tworzymy etykiete - pozniej sie ja albo zmodyfikuje albo wywali teraz do testow jest
lbl = Label(app,text ="taki sobie tekst etykiety ktorego zmienic nie mozna")

# jak wyjasnic co to jewst grid? niby podswiadomie się orientuje to jakis 'wyzwalacz' ktory uruchamia  ale czy aby na pewno??
lbl.grid()

# no to zrobmy jakis przycisk a nie sama etykiete...
bttnl = Button(app, text = "kolejny glupi tekst na nic nie robiącym przycisku.")
# aktywujemy BTTNL
bttnl.grid()





root.mainloop()