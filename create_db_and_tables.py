import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_stuff(database):

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""


    sql_create_book_table="""CREATE TABLE books(
	                                book_id INTEGER  NOT NULL  PRIMARY KEY AUTOINCREMENT,
	                                book_serial text NOT NULL,
                                    book_name text NOT NULL
                                );"""

    sql_create_writer_table="""CREATE TABLE writers(
	                            writer_id INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
                                writer_name text NOT NULL
                            );"""

    sql_create_year_table="""CREATE TABLE publ_year(
	                            year_id INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT, 
	                            pub_year INTEGER  NOT NULL UNIQUE
                            );"""

    sql_create_edition_table="""CREATE TABLE edition(
	                            ed_id INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
                                edition text NOT NULL UNIQUE
                            );"""

    sql_create_genre_table="""CREATE TABLE genre(
	                            genre_id INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
                                genre text NOT NULL UNIQUE,
                                genre_code text NOT NULL UNIQUE,
                                genre_serial text UNIQUE
                            );"""

    sql_create_book_genre_table="""CREATE TABLE book_genre(
	                                id INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    book_id INT,
                                    genre_id INT,
                                    FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE,
                                    FOREIGN KEY(genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE
                                );"""

    sql_create_book_writer_table="""CREATE TABLE book_writer(
	                                id INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    book_id INT,
                                    writer_id INT,
                                    FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE,
                                    FOREIGN KEY(writer_id) REFERENCES writers(writer_id) ON DELETE CASCADE
                                );"""

    sql_create_book_year_table="""CREATE TABLE book_year(
	                                id INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    book_id INTEGER ,
                                    year_id INTEGER ,
                                    FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE,
                                    FOREIGN KEY(year_id) REFERENCES publ_year(year_id) ON DELETE CASCADE
                                );"""

    sql_create_book_ed_table="""CREATE TABLE book_ed(
	                                id INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    book_id INTEGER ,
                                    ed_id INTEGER ,
                                    FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE,
                                    FOREIGN KEY(ed_id) REFERENCES edition(ed_id) ON DELETE CASCADE
                                );"""

    sql_create_view_allrecords="""CREATE VIEW allRecords AS
	                                SELECT
		                                genre.genre as genre,
                                        genre.genre_code as genre_code,
                                        genre.genre_serial as genre_serial,
                                        books.book_serial as book_serial,
                                        books.book_name as book_name,
                                        writers.writer_name as writer_name,
                                        edition.edition as edition,
                                        publ_year.pub_year as pub_year
	                                FROM genre
		                                INNER JOIN book_genre ON genre.genre_id=book_genre.genre_id
                                        INNER JOIN books ON book_genre.book_id=books.book_id
                                        INNER JOIN book_writer ON books.book_id=book_writer.book_id
                                        INNER JOIN writers ON book_writer.writer_id=writers.writer_id
                                        INNER JOIN book_ed ON books.book_id=book_ed.book_id
                                        INNER JOIN edition ON book_ed.ed_id=edition.ed_id
                                        INNER JOIN book_year ON books.book_id=book_year.book_id
                                        INNER JOIN publ_year ON book_year.year_id=publ_year.year_id
	                                ORDER BY genre.genre_id;"""
                                
                                # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)

        create_table(conn, sql_create_book_table)
        create_table(conn, sql_create_writer_table)
        create_table(conn, sql_create_year_table)
        create_table(conn, sql_create_edition_table)
        create_table(conn, sql_create_genre_table)
        create_table(conn, sql_create_book_genre_table)
        create_table(conn, sql_create_book_writer_table)
        create_table(conn, sql_create_book_year_table)
        create_table(conn, sql_create_book_ed_table)
        create_table(conn, sql_create_view_allrecords)


    else:
        print("Error! cannot create the database connection.")
