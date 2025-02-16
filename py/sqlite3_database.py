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


def bookcase_test_table_structure(database_name,table_name_for_test):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = "PRAGMA table_info ("+str(table_name_for_test)+");"
  print(sql_query)
  cursor = sqliteConnection.cursor()
  cursor.execute(str(sql_query))
  print("Tables ",table_name_for_test," structure:\n")
  print(cursor.fetchall())


def bookcase_test_table_AUTHOR_structure(database_name):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = "PRAGMA table_info (AUTHOR);"
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
#  print(sql_query)
  print("Tables AUTHOR structure:\n")
  print(cursor.fetchall())

def bookcase_test_table_BOOK_structure(database_name):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = "PRAGMA table_info (BOOK);"
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
#  print(sql_query)
  print("Tables BOOK structure:\n")
  print(cursor.fetchall())

def bookcase_test_table_COMIC_structure(database_name):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = "PRAGMA table_info (COMIC);"
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
#  print(sql_query)
  print("Tables COMIC structure:\n")
  print(cursor.fetchall())

def bookcase_test_table_COMPANY_structure(database_name):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = "PRAGMA table_info (COMPANY);"
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
#  print(sql_query)
  print("Tables COMPANY structure:\n")
  print(cursor.fetchall())

def bookcase_test_table_EBOOK_structure(database_name):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = "PRAGMA table_info (EBOOK);"
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
#  print(sql_query)
  print("Tables EBOOK structure:\n")
  print(cursor.fetchall())

def bookcase_test_table_MOVIE_structure(database_name):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = "PRAGMA table_info (MOVIE);"
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
#  print(sql_query)
  print("Tables MOVIE structure:\n")
  print(cursor.fetchall())

def bookcase_test_table_VIDEO_GAME_structure(database_name):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = "PRAGMA table_info (VIDEO_GAME);"
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
#  print(sql_query)
  print("Tables VIDEO_GAME structure:\n")
  print(cursor.fetchall())

#def bookcase_test_table_XXXXX_structure(database_name):
#  sqliteConnection = sqlite3.connect(database_name)
#  sql_query = "PRAGMA table_info (XXXXX);"
#  cursor = sqliteConnection.cursor()
#  cursor.execute(sql_query)
##  print(sql_query)
#  print("Tables XXXXX structure:\n")
#  print(cursor.fetchall())


def bookcase_create_AUTHOR_table(database_name):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = """ CREATE TABLE AUTHOR ( ID INTEGER PRIMARY KEY AUTOINCREMENT , FIRSTNAME TEXT, LASTNAME TEXT );"""
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
  print("Created table\n")
  print(cursor.fetchall())

def bookcase_create_BOOK_table(database_name):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = """CREATE TABLE BOOK ( ID INTEGER PRIMARY KEY AUTOINCREMENT , 
                                      ADDITIONAL_AUTHORS TEXT, 
                                      AMAZON_URL TEXT, 
                                      AUTHOR INTEGER, 
                                      CATEGORIES TEXT, 
                                      COMMENTS TEXT, 
                                      COVER_PATH TEXT, 
                                      FNAC_URL TEXT, 
                                      TITLE TEXT, 
                                      ISBN TEXT, 
                                      PAGES INTEGER, 
                                      PUBLISHED_DATE TEXT, 
                                      PUBLISHER TEXT, 
                                      SUMMARY TEXT, 
                                      READING_DATES TEXT, 
                                      SERIES TEXT, 
                                      READ INTEGER, 
                                      IN_WISHLIST INTEGER );"""
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
  print("Table ""BOOK"" created\n")
  print(cursor.fetchall())

def bookcase_create_COMIC_table(database_name):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = """ CREATE TABLE COMIC ( ID INTEGER PRIMARY KEY AUTOINCREMENT , 
                                      ADDITIONAL_AUTHORS TEXT, 
                                      AMAZON_URL TEXT, 
                                      AUTHOR INTEGER, 
                                      CATEGORIES TEXT, 
                                      COMMENTS TEXT, 
                                      COVER_PATH TEXT, 
                                      FNAC_URL TEXT, 
                                      TITLE TEXT, 
                                      ISBN TEXT, 
                                      PAGES INTEGER, 
                                      PUBLISHED_DATE TEXT, 
                                      PUBLISHER TEXT, 
                                      SUMMARY TEXT, 
                                      READING_DATES TEXT, 
                                      SERIES TEXT, 
                                      READ INTEGER, 
                                      IN_WISHLIST INTEGER );"""
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
  print("Table ""COMIC"" created\n")
  print(cursor.fetchall())

def bookcase_create_COMPANY_table(database_name):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = """ CREATE TABLE COMPANY ( ID INTEGER PRIMARY KEY AUTOINCREMENT , NAME TEXT );"""
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
  print("Table ""COMPANY"" created\n")
  print(cursor.fetchall())

def bookcase_create_EBOOK_table(database_name):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = """ ;"""
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
  print("Table ""EBOOK"" created\n")
  print(cursor.fetchall())

def bookcase_create_MOVIE_table(database_name):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = """ CREATE TABLE MOVIE ( ID INTEGER PRIMARY KEY AUTOINCREMENT , 
                                        ADDITIONAL_DIRECTORS TEXT, 
                                        AMAZON_URL TEXT, 
                                        CATEGORIES TEXT, 
                                        COMMENTS TEXT, 
                                        COVER_PATH TEXT, 
                                        DIRECTOR INTEGER, 
                                        EAN TEXT, 
                                        FORMAT TEXT, 
                                        IN_WISHLIST INTEGER, 
                                        PRODUCTION_COMPANY TEXT, 
                                        PUBLISHED_DATE TEXT, 
                                        SEEN INTEGER, 
                                        SERIES TEXT, 
                                        SUMMARY TEXT, 
                                        TITLE TEXT, 
                                        VIEWING_DATES TEXT );"""
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
  print("Table ""MOVIE"" created\n")
  print(cursor.fetchall())

def bookcase_create_VIDEO_GAME_table(database_name):
  sqliteConnection = sqlite3.connect(database_name)
  sql_query = """ CREATE TABLE VIDEO_GAME ( ID INTEGER PRIMARY KEY AUTOINCREMENT , 
                                            ADDITIONAL_DEVELOPERS TEXT, 
                                            AMAZON_URL TEXT, 
                                            CATEGORIES TEXT, 
                                            COMMENTS TEXT, 
                                            COVER_PATH TEXT, 
                                            DEVELOPER INTEGER, 
                                            EAN TEXT, 
                                            TITLE TEXT, 
                                            PLATFORM TEXT, 
                                            SUMMARY TEXT, 
                                            PLAYED_DATES TEXT, 
                                            PUBLISHED_DATE TEXT, 
                                            PUBLISHER TEXT, 
                                            SERIES TEXT, 
                                            PLAYED INTEGER, 
                                            IN_WISHLIST INTEGER );"""
  cursor = sqliteConnection.cursor()
  cursor.execute(sql_query)
  print("Table ""VIDEO_GAME"" created\n")
  print(cursor.fetchall())

#def bookcase_create_XXXXX_table(database_name):
#  sqliteConnection = sqlite3.connect(database_name)
#  sql_query = """ CREATE TABLE XXXXX ( // polecenie tworzace tabele tutaj // );"""
#  cursor = sqliteConnection.cursor()
#  cursor.execute(sql_query)
#  print("Created table\n")
#  print(cursor.fetchall())


# tymczasowo dla testów
sqlite3_test_connect('mylibrary.db')
#bookcase_test_database_structure('mylibrary.db')
#bookcase_test_table_AUTHOR_structure('mylibrary.db')
#bookcase_test_table_BOOK_structure('mylibrary.db')
#bookcase_test_table_COMIC_structure('mylibrary.db')
#bookcase_test_table_COMPANY_structure('mylibrary.db')
#bookcase_test_table_EBOOK_structure('mylibrary.db')
#bookcase_test_table_MOVIE_structure('mylibrary.db')
#bookcase_test_table_VIDEO_GAME_structure('mylibrary.db')
#bookcase_test_table_XXXXX_structure('mylibrary.db')
bookcase_test_table_structure('mylibrary.db','AUTHOR')
bookcase_test_table_structure('mylibrary.db','BOOK')
bookcase_test_table_structure('mylibrary.db','COMIC')
bookcase_test_table_structure('mylibrary.db','COMPANY')
bookcase_test_table_structure('mylibrary.db','AUTHOR')
#bookcase_create_AUTHOR_table('mylibrary_test.db')
#bookcase_create_BOOK_table('mylibrary_test.db')
#bookcase_create_COMIC_table('mylibrary_test.db')
#bookcase_create_COMPANY_table('mylibrary_test.db')
#bookcase_create_EBOOK_table('mylibrary_test.db')
#bookcase_create_MOVIE_table('mylibrary_test.db')
#bookcase_create_VIDEO_GAME_table('mylibrary_test.db')
##bookcase_create_XXXXX_table('mylibrary_test.db')
