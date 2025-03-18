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
#app - to obszar roboczy aaplikacji - innymi słowy całe wnętrze ramki...


# tworzymy etykiete - pozniej sie ja albo zmodyfikuje albo wywali teraz do testow jest
#lbl = Label(app,text ="taki sobie tekst etykiety ktorego zmienic nie mozna")

# jak wyjasnic co to jewst grid? niby podswiadomie się orientuje to jakis 'wyzwalacz' ktory uruchamia  ale czy aby na pewno??
#lbl.grid()

# no to zrobmy jakis przycisk a nie sama etykiete...
#bttnl = Button(app, text = "kolejny glupi tekst na nic nie robiącym przycisku.")
# aktywujemy BTTNL
#bttnl.grid()

# drugi przycisk - pusty
#bttn2 = Button(app)

#modyfikujemy przycisk 2
#bttn2.configure(text="skleroza nie boli tylko trzeba sie nachodzić, albo napisc ...")
#bttn2.grid()


#bttn3 = Button(app,text="trzeci guzik")
#bttn3.grid()

#zaczynamy dzielic ekran pod uklad przyciskow...
#dlaczego dzieli jakbt chcialo a nie moglo ...?
# widac to na dacie wydania..
app.grid(row=8,column=4,columnspan=2, sticky=W)

# no to zobaczymy jak bardzo pjetnym debilem jestem ....
# =================================================================================================================================
# wiersz 1-szy
# ISBN
# ISBN ksiazki
ISBN13_lbl_def = Label(text="ISBN: ")
# i jak rozumiem to mam podac lokalizacje: ktory wiersz, ktora kolumna i to 'sticky - czyli wyrownanie
ISBN13_lbl_def.grid(row=1,column=0,sticky=W)
# tu sie powinno pojawic potem wybrany ISBN....
ISBN13_lbl_value = Label(text="1234567890123")
ISBN13_lbl_value.grid(row=1, column=1,sticky=W)

#===================================================================================================================================
#wiersz 2
# "Autor: "; autor imie i nazwisko
author_lbl_text = Label(text="Autor: ")
author_lbl_text.grid(row=2, column=0, sticky=W)

# tu poprawić, żeby imie i nazwisko było jednym cięgiem ....
author_imie_val = Label(text="dowolne bzdury, bedzie imie autora")
author_imie_val.grid(row=2, column=1, sticky=W)
author_nazwisko_val = Label(text="dowolne bzdury, bedzie nazwisko autora")
author_nazwisko_val.grid(row=2, column=2, sticky=W)

#wiersz 2A
# jak jest więcej autorow to kolejny autor,

#tu by trzeba ustawić zliczanie wierszy....
#jeśli jest więcej niż jeden autor ....

# jesli nie to to:
#========================================================================================================================================
#wiersz 3
# "tytuł: "; pelny tytul pozycji
title_lbl_text = Label(text="Tytuł: ")
title_lbl_text.grid(row=3, column=0, sticky=W)
title_lbl_val = Label(text="teraz jest wpis z palca, potem bedzie to co jest w bazie")
title_lbl_val.grid(row=3, column=1, sticky=W)

#==========================================================================================================================================
#wiersz 4
#"Wydawca "; nazwa wydawcy; "Rok wydania: "; rok_wydania
publisher_lbl_text = Label(text="Publisher: ")
publisher_lbl_text.grid(row=4,column=0,sticky=W)
publisher_lbl_t2 = Label(text="teraz jest byle co, potem bedzie wartosc pobrana z bazy danych ...")
publisher_lbl_t2.grid(row=4,column=1,sticky=W)

#rok wydania
publish_date_lbl_def = Label(text="Data wydania: ")
publish_date_lbl_def.grid(row=4, column=2,sticky=W)
publish_date_lbl_t2 = Label(text="2025, ale docelowoo bedzie data wydania")
publish_date_lbl_t2.grid(row=4, column=3,sticky=W)

#==========================================================================================================================================
# wiersz 5
#ilość stron 
il_stron_lbl_text = Label(text="Pages: ")
il_stron_lbl_text.grid(row=5, column=0,sticky=W)
il_stron_lbl_val = Label(text="tu ilość stron np. 235, potem będzie zapełnione faktyczną wartością")
il_stron_lbl_val.grid(row=5,column=1,sticky=W)

#które wydanie (?)
nr_wydania_lbl_text = Label(text=" Wydanie: ")
nr_wydania_lbl_text.grid(row=5,column=2,sticky=W)
nr_wydania_lbl_val = Label(text=("tu numer wydania jesli nie będzie to puste"))
nr_wydania_lbl_val.grid(row=5,column=3,sticky=W)
#=========================================================================================================================================
#jaka seria (o ile)

#krótki opis

# no dobra patrząc na to p czym rozmawialiśmy wczoraj tj. w poniedziałęk,
# Tu powinienem zebrać w całości to co wiem o książce i zroić z tego duuuuży string..


root.mainloop()