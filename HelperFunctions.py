from ClassRecords import *
import sys
import traceback
from wx.adv import NotificationMessage
import wx
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    db = None
    try:
        db = sqlite3.connect(db_file)
        return db
    except Error as e:
        print(e)

    return db




def get_genre_info(db):
    cursor=db.cursor()
    #cursor.execute("USE %s" % self.db_name)  

    #Pre-load Existing Genre information
    genre_info=list() 
    
    cursor.execute("SELECT genre,genre_code,genre_serial FROM Genre")
    #cursor.execute("SELECT DISTINCT genre,genre_code,genre_serial FROM allrecords")
    records = cursor.fetchall()

    for record in records:
        genre_info.append(Genre(record[0],record[1],record[2]))

    cursor.close()
    return genre_info
#############################################################################################



def searchSpecificEntryFromDB(db,gen_name,book_name,writer_name):
    cursor=db.cursor()
#The queries here are in correct way, prevents SQL injection    
    if(len(gen_name)>0 and len(book_name)>0 and len(writer_name)==0):
        sql_command="SELECT * FROM allrecords where genre=? AND book_name Like ?"
        params = (gen_name, "%"+book_name+"%")
        cursor.execute(sql_command,params)
    elif(len(gen_name)>0 and len(book_name)==0 and len(writer_name)>0):
        sql_command="SELECT * FROM allrecords where genre=? AND writer_name Like ?"
        params = (gen_name, "%"+writer_name+"%")
        cursor.execute(sql_command,params)
    elif(len(gen_name)>0 and len(book_name)==0 and len(writer_name)==0):
        sql_command="SELECT * FROM allrecords where genre=?"
        params = (gen_name,)
        cursor.execute(sql_command,params)
    
    elif(len(gen_name)==0 and len(book_name)>0 and len(writer_name)>0):
        sql_command="SELECT * FROM allrecords where book_name  Like ? AND writer_name Like ?"
        params = ("%"+book_name+"%", "%"+writer_name+"%")
        cursor.execute(sql_command,params)
    elif(len(gen_name)==0 and len(book_name)>0 and len(writer_name)==0):
        sql_command="SELECT * FROM allrecords where book_name Like ?"
        params = ("%"+book_name+"%",)
        cursor.execute(sql_command,params)

    elif(len(gen_name)==0 and len(book_name)==0 and len(writer_name)>0):
        sql_command="SELECT * FROM allrecords where writer_name Like ?"
        params = ("%"+writer_name+"%",)
        cursor.execute(sql_command,params)
    else:
        pass
    try:
        results=cursor.fetchall()
    except:
        results=list()

    cursor.close()
    return results

def searchAllEntryFromDB(db):
    cursor=db.cursor()
    sql_command="SELECT * FROM allrecords"
    cursor.execute(sql_command)
    try:
        results=cursor.fetchall()
    except:
        results=list()

    cursor.close()
    return results



##############################################################


def __get_book_serial(db,gen_serial):
    book_serial=list()
    cursor=db.cursor()
    #TODO: Add code to protect no input from USER(May refer to User not interested in / don't know genre, affects book serial section also )
    sql_command="SELECT book_serial FROM allrecords WHERE genre_serial = ?"
    params=(str(gen_serial),);
    cursor.execute(sql_command,params)
    records = cursor.fetchall()
    ## Showing the data
    for record in records:
        book_serial.append(record[0])
    if(len(book_serial)==0):
        cursor.close()
        return gen_serial+'-'+str(1)
    else:
        for i in range(len(book_serial)):
            book_serial[i]=book_serial[i].split('-',1)[1]
            book_serial[i]=int(book_serial[i])
    
        book_serial.sort(reverse=True)
        cursor.close()
        return gen_serial+'-'+str(book_serial[0]+1)


def __createEntry(db,genre_info,gen_name,gen_code,gen_serial,book_name,writer_name,edition,publ_year):
    gen_name_list=list()
    for gen_inf in genre_info:
        gen_name_list.append(gen_inf.genre)

#TODO, handle unknown genre, gotta be able to edit those
#TODO: change genre verification method. this is taken from the view, which is unioned. creating clutter, check from genre table in db

    if gen_name in gen_name_list:
        idx=gen_name_list.index(gen_name)
        gen_code=genre_info[idx].genre_code
        gen_serial=genre_info[idx].genre_serial
        new_genre=False
    else:
        new_genre=True
    
    book_serial=__get_book_serial(db,gen_serial)

    publ_year=int(publ_year)
    book=Book(book_name,book_serial,edition,publ_year,writer_name)
    genre=Genre(gen_name,gen_code,gen_serial,new_genre)
    entry=DbEntry(genre,book)

    return entry


def __insert_sql(sql_command,params,db):
    cursor=db.cursor()
    cursor.execute(sql_command,params)
    cursor.execute("SELECT last_insert_rowid()")
    temp=cursor.fetchall()
    cursor.close()
    return temp[0][0]



#In gui, this function will be called to add an entry
def addEntryToDB(db,genre_info,gen_name,gen_code,gen_serial,book_name,writer_name,edition,publ_year,book_serial=0):
    entry=__createEntry(db,genre_info,gen_name,gen_code,gen_serial,book_name,writer_name,edition,publ_year)

    cursor=db.cursor()
    #At this point everything should be verified, now time to insert into database
    if (book_serial!=0):
        entry.book.book_serial=book_serial
    #print(entry.genre.genre,
    #      entry.genre.genre_code,
    #      entry.genre.genre_serial,
    #      entry.book.book_name,
    #      entry.book.book_serial,
    #      entry.book.writer,
    #      entry.book.book_ed,
    #      entry.book.publ_year)
    
    #modify for prevention of injection attack
    #https://stackoverflow.com/questions/51647301/how-do-pymysql-prevent-user-from-sql-injection-attack

    sql_command="INSERT INTO books(book_serial,book_name) VALUES(?,?)"
    params = (entry.book.book_serial,entry.book.book_name)
    book_id=__insert_sql(sql_command,params,db)

    sql_command="SELECT writer_id FROM writers WHERE writer_name=?"
    params=(entry.book.writer,)
    cursor.execute(sql_command,params)
    temp=cursor.fetchall()

    if not temp:
        sql_command="INSERT INTO writers(writer_name) VALUES(?)"
        params = (entry.book.writer,)
        writer_id=__insert_sql(sql_command,params,db)
    else:
        writer_id=temp[0][0]

    sql_command="SELECT ed_id FROM edition WHERE edition=?"
    params=(entry.book.book_ed,)
    cursor.execute(sql_command,params)
    temp=cursor.fetchall()

    if not temp:
        sql_command="INSERT INTO edition(edition) VALUES(?)"
        params = (entry.book.book_ed,)
        ed_id=__insert_sql(sql_command,params,db)
    else:
        ed_id=temp[0][0]

    sql_command="SELECT year_id FROM publ_year WHERE pub_year=?"
    params=(publ_year,)
    cursor.execute(sql_command,params)
    temp=cursor.fetchall()

    if not temp:
        sql_command="INSERT INTO publ_year(pub_year) VALUES(?)"
        params=(entry.book.publ_year,)
        year_id=__insert_sql(sql_command,params,db)
    else:
        year_id=temp[0][0]

    if entry.genre.new_genre:

        sql_command="INSERT INTO genre(genre,genre_code,genre_serial) VALUES(?,?,?)"
        params=(entry.genre.genre,entry.genre.genre_code,entry.genre.genre_serial)
        genre_id=__insert_sql(sql_command,params,db)
    else:

        sql_command="SELECT genre_id FROM genre WHERE genre_serial = ?" 
        params=(entry.genre.genre_serial,);
        cursor.execute(sql_command,params)
        temp=cursor.fetchall()
        genre_id=temp[0][0]
    

    sql_command="INSERT INTO book_genre(book_id,genre_id) VALUES(?,?)" 
    params=(book_id,genre_id)
    cursor.execute(sql_command,params)
    sql_command="INSERT INTO book_writer(book_id,writer_id) VALUES(?,?)"
    params=(book_id,writer_id)
    cursor.execute(sql_command,params)
    sql_command="INSERT INTO book_year(book_id,year_id) VALUES(?,?)"
    params=(book_id,year_id)
    cursor.execute(sql_command,params)
    sql_command="INSERT INTO book_ed(book_id,ed_id) VALUES(?,?)"
    params=(book_id,ed_id)
    cursor.execute(sql_command,params)
    cursor.close()
    db.commit()

###################################################################
def deleteFromDB(db,book_name):
    cursor=db.cursor()
    try:
        sql_command="DELETE FROM books WHERE book_name=?"
        params=(book_name,)
        cursor.execute(sql_command,params)
        db.commit()
        __cleanup_empty_values(db)
        return 1
    except(Exception):
        ex_type, ex_value, ex_traceback = sys.exc_info()

        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)

        # Format stacktrace
        stack_trace = list()

        for trace in trace_back:
            stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

        print("Exception type : %s " % ex_type.__name__)
        print("Exception message : %s" %ex_value)
        print("Stack trace : %s" %stack_trace)
        return 0

##################################################################################
def _getOldEntryInfo(db,old_entry):
    cursor=db.cursor()

    #ensures a single record
    sql_command="SELECT book_serial FROM allrecords WHERE book_name=? AND writer_name=?"
    params=(old_entry[4],old_entry[5])
    cursor.execute(sql_command,params)
    old_book_serial=cursor.fetchall()[0][0]

    sql_command="SELECT book_id FROM books WHERE book_serial=?"
    params=(old_book_serial,)
    cursor.execute(sql_command,params)
    old_book_id=cursor.fetchall()[0][0]

    sql_command="SELECT genre_id FROM book_genre WHERE book_id=?"
    params=(old_book_id,)
    cursor.execute(sql_command,params)
    old_gen_id=cursor.fetchall()[0][0]


    sql_command="SELECT ed_id FROM book_ed WHERE book_id=?"
    params=(old_book_id,)
    cursor.execute(sql_command,params)
    old_ed_id=cursor.fetchall()[0][0]

    sql_command="SELECT writer_id FROM book_writer WHERE book_id=?"
    params=(old_book_id,)
    cursor.execute(sql_command,params)
    old_writer_id=cursor.fetchall()[0][0]

    old_id_dic = {
        "old_book_serial":old_book_serial,
        "old_gen_id": old_gen_id,
        "old_book_id": old_book_id,
        "old_ed_id": old_ed_id,
        "old_writer_id": old_writer_id
        }
    return old_id_dic

def editDbEntry(db,genre_info,genre,genre_code,genre_serial,book_serial,book_name,writer_name,edition,publ_year,old_entry,parent):
    try:
        old_id_dic=_getOldEntryInfo(db,old_entry)
        old_gen_id=old_id_dic.get("old_gen_id")
        old_book_id=old_id_dic.get("old_book_id")
        old_book_serial=old_id_dic.get("old_book_serial")
        cursor=db.cursor()
        if genre.lower()!=old_entry[0].lower():
            sql_command="SELECT genre_id,genre_serial FROM genre where genre=?"
            params=(genre,)
            cursor.execute(sql_command,params)
            temp=cursor.fetchall()
            new_gen_id=temp[0][0]
            new_gen_serial=temp[0][1]
        

            new_book_serial=__get_book_serial(db,new_gen_serial)
       
            sql_command="UPDATE book_genre SET genre_id=? WHERE genre_id=? and book_id=?"
            params=(new_gen_id,old_gen_id,old_book_id)
            cursor.execute(sql_command,params)

            sql_command="UPDATE books SET book_serial=? WHERE book_id=?"
            params=(new_book_serial,old_book_id)
            cursor.execute(sql_command,params)
            db.commit()
    
        if(book_name.lower()!=old_entry[4].lower()):
            sql_command="UPDATE books SET book_name=? WHERE book_id=?"
            params=(book_name,old_book_id)
            cursor.execute(sql_command,params)
            db.commit()

        if(writer_name.lower()!=old_entry[5].lower()):
            sql_command="SELECT writer_id FROM writers WHERE writer_name=?"
            params=(writer_name,)
            cursor.execute(sql_command,params)
            temp=cursor.fetchall()
        
            if not temp:
                sql_command="INSERT INTO writers(writer_name) VALUES(?)"
                params = (writer_name,)
                new_writer_id=__insert_sql(sql_command,params,db)
                sql_command="UPDATE book_writer SET writer_id=? WHERE book_id=?"
                params=(new_writer_id,old_book_id)
                cursor.execute(sql_command,params)
                db.commit()
            else:
                sql_command="UPDATE book_writer SET writer_id=? WHERE book_id=?"
                params=(temp[0][0],old_book_id)
                cursor.execute(sql_command,params)
                db.commit()


        if(edition.lower()!=old_entry[6].lower()):
            sql_command="SELECT ed_id FROM edition WHERE edition=?"
            params=(edition,)
            cursor.execute(sql_command,params)
            temp=cursor.fetchall()
        
            if not temp:
                sql_command="INSERT INTO edition(edition) VALUES(?)"
                params = (edition,)
                new_ed_id=__insert_sql(sql_command,params,db)
                sql_command="UPDATE book_ed SET ed_id=? WHERE book_id=?"
                params=(new_ed_id,old_book_id)
                cursor.execute(sql_command,params)
                db.commit()
            else:
                sql_command="UPDATE book_ed SET ed_id=? WHERE book_id=?"
                params=(temp[0][0],old_book_id)
                cursor.execute(sql_command,params)
                db.commit()

        if(publ_year!=old_entry[7]):
            sql_command="SELECT year_id FROM publ_year WHERE pub_year=?"
            params=(publ_year,)
            cursor.execute(sql_command,params)
            temp=cursor.fetchall()
        
            if not temp:
                sql_command="INSERT INTO publ_year(pub_year) VALUES(?)"
                params = (publ_year,)
                new_year_id=__insert_sql(sql_command,params,db)
                sql_command="UPDATE book_year SET year_id=? WHERE book_id=?"
                params=(new_year_id,old_book_id)
                cursor.execute(sql_command,params)
                db.commit()
            else:
                sql_command="UPDATE book_year SET year_id=? WHERE book_id=?"
                params=(temp[0][0],old_book_id)
                cursor.execute(sql_command,params)
                db.commit()
    
        if(book_serial.lower()!=old_entry[3].lower() and genre.lower()==old_entry[0].lower()):
            sql_command="SELECT book_serial FROM books WHERE book_serial=?"
            params=(book_serial,)
            cursor.execute(sql_command,params)
            temp=cursor.fetchall()
        
            if not temp:
                sql_command="UPDATE books SET book_serial=? WHERE book_id=?"
                params=(book_serial,old_book_id)
                cursor.execute(sql_command,params)
            else:
                nm=NotificationMessage(title='',message='Serial number already in use',parent=parent)
                nm.Show(timeout=wx.adv.NotificationMessage.Timeout_Auto)
                raise Exception("Serial number already in use")
        
        __cleanup_empty_values(db)
        return True
    except Exception as e:
        #print(e)
        return False

def __cleanup_empty_values(db):
    
    cursor=db.cursor()
    sql_command="SELECT genre FROM genre"
    cursor.execute(sql_command)
    temp=cursor.fetchall()
    mainGen=list()
    for value in temp:
        mainGen.append(value[0])
    
    
    sql_command="SELECT genre FROM allrecords"
    cursor.execute(sql_command)
    temp=cursor.fetchall()
    viewGen=list()
    for value in temp:
        viewGen.append(value[0])

    for i in range(len(mainGen)):
        if mainGen[i] not in viewGen:
            sql_command="DELETE FROM genre WHERE genre=?"
            params=(mainGen[i],)
            cursor.execute(sql_command,params)
            db.commit()


    sql_command="SELECT writer_name FROM writers"
    cursor.execute(sql_command)
    temp=cursor.fetchall()
    mainWriter=list()
    for value in temp:
        mainWriter.append(value[0])
    
    sql_command="SELECT writer_name FROM allrecords"
    cursor.execute(sql_command)
    temp=cursor.fetchall()
    viewWriter=list()
    for value in temp:
        viewWriter.append(value[0])

    for i in range(len(mainWriter)):
        if mainWriter[i] not in viewWriter:
            sql_command="DELETE FROM writers WHERE writer_name=?"
            params=(mainWriter[i],)
            cursor.execute(sql_command,params)
            db.commit()

    sql_command="SELECT edition FROM edition"
    cursor.execute(sql_command)
    temp=cursor.fetchall()
    mainEd=list()
    for value in temp:
        mainEd.append(value[0])
    
    sql_command="SELECT edition FROM allrecords"
    cursor.execute(sql_command)
    temp=cursor.fetchall()
    viewEd=list()
    for value in temp:
        viewEd.append(value[0])

    for i in range(len(mainEd)):
        if mainEd[i] not in viewEd:
            sql_command="DELETE FROM edition WHERE edition=?"
            params=(mainEd[i],)
            cursor.execute(sql_command,params)
            db.commit()


    sql_command="SELECT pub_year FROM publ_year"
    cursor.execute(sql_command)
    temp=cursor.fetchall()
    mainYear=list()
    for value in temp:
        mainYear.append(value[0])
    
    sql_command="SELECT pub_year FROM allrecords"
    cursor.execute(sql_command)
    temp=cursor.fetchall()
    viewYear=list()
    for value in temp:
        viewYear.append(value[0])

    for i in range(len(mainYear)):
        if mainYear[i] not in viewYear:
            sql_command="DELETE FROM publ_year WHERE pub_year=?"
            params=(mainYear[i],)
            cursor.execute(sql_command,params)
            db.commit()
    cursor.close()