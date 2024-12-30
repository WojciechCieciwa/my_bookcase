import sqlite3

def sqlite3_test_connect(database_name):
    sqliteConnection = sqlite3.connect(database_name)
    cursor = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")

    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("SQLite Database Version is: ", record)
    #cursor.close()

# sprawdzanie czy sa odpowiednie tablice ...
# obowiązkowe: author, book, company
# uzupełniające: comoc, ebook, movie, video_game

def bookcase_test_database_structure(database_name):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = """SELECT name FROM sqlite_master 
    WHERE type='table';"""
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
  print("List of tables\n")
  print(cursor.fetchall())

def bookcase_test_table_structure(database_name, table_name):
  sqliteConnection = sqlite3.connect(database_name)
#  sql_query = """SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
#    WHERE table_name = 'table_name';"""
  sql_query = "PRAGMA table_info('table_name');"
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
  print("Tables",table_name,"structure:\n")
  print(cursor.fetchall())
 #


# tymczasowo dla testów
sqlite3_test_connect('mylibrary.db')
bookcase_test_database_structure('mylibrary.db')
bookcase_test_table_structure('mylibrary.db', "AUTHOR")