import sqlite3
from sqlite3 import Error
from create_db_and_tables import *
from LoadFromExcel import loadFromExcel

#def main():
    database = r"D:\Lib_sqlite\Library_sqlite\personal_library.db"

    conn=create_connection(database)
    loadFromExcel(conn)


#if __name__ == '__main__':
#    main()
#

