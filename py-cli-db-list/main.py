from db_processing import DatabaseHandler, DBNavigator


def main():
    # init db
    db_handler = DatabaseHandler()
    file_path = "mylibrary.db"
    db_handler.load_file(file_path)
    db_navigator = DBNavigator(db_handler)
    # reset navigation to init state
    db_navigator.reset_navigation()
    # process tables
    for t in db_navigator.tables:
        print (t)
        # process columns in current table
        columns = db_navigator.get_table_columns(t)
        for c in columns:
            print (f"    " + c)


if __name__ == "__main__":
    main()
