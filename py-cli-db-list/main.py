from db_processing import DatabaseHandler, DBNavigator


def main():
    # load db
    db_handler = DatabaseHandler()
    file_path = "mylibrary.db"
    db_handler.load_file(file_path)
    db_navigator = DBNavigator(db_handler)
    db_navigator.reset_navigation()
    # display tables
    for t in db_navigator.tables:
        print (t)
        columns = db_navigator.get_table_columns(t)
        for c in columns:
            print (f"    " + c)
    # select table
    # show columns in a selected table


if __name__ == "__main__":
    main()
