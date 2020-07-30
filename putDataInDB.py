def put_data_in_db(db,df,genre):
    import sqlite3
    from sqlite3 import Error
    import pandas as pd
    from LoadFromExcel import unique_col_val

    cursor=db.cursor()


    #Insert into Books
    for index, row in df.iterrows():
        num=row['serial_num']
        name=row['Name']
        book_id=row['book_id']
        num=num.strip()
        name=name.strip()
        #num='"'+num+'"'
        #name='"'+name+'"'
        sql_command="INSERT INTO books(book_id,book_serial,book_name) VALUES(?,?,?)"
        params=(book_id,num,name)
        cursor.execute(sql_command,params)

    # Insert Writers
    writers=unique_col_val(df,'Author')
    writers_id=[i for i in range(1,len(writers)+1)] 
    for i in range(len(writers)):
        name=writers[i]
        writ_id=writers_id[i]
        name=name.strip()
        #name='"'+name+'"'
        sql_command="INSERT INTO writers(writer_id,writer_name) VALUES(?,?)" 
        params=(writ_id,name)
        cursor.execute(sql_command,params)
    
    # Insert into edition

    edition=unique_col_val(df,'Edition')
    edition_id=[i for i in range(1,len(edition)+1)]    
    for i in range(len(edition)):
        ed=edition[i]
        print(ed)
        ed_id=edition_id[i]
        ed=ed.strip()
        #ed='"'+ed+'"'
        sql_command="INSERT INTO edition(ed_id,edition) VALUES(?,?)" 
        params=(ed_id,ed)
        cursor.execute(sql_command,params)
    
    # Insert into year
    year=unique_col_val(df,'Year')
    year_id=[i for i in range(1,len(year)+1)]    
    for i in range(len(year)):
        yr=year[i]
        yr_id=year_id[i]
        sql_command="INSERT INTO publ_year(year_id,pub_year) VALUES(?,?)" 
        params=(yr_id,yr)
        cursor.execute(sql_command,params)
    
        
    #Insert into Genre
    for index, row in genre.iterrows():
        genre_name=row['Genre']
        genre_code=row['Genre_code']
        genre_serial=row['Genre_serial']
        genre_id=row['Genre_id']
        genre_name=genre_name.strip()
        genre_code=genre_code.strip()
        genre_serial=genre_serial.strip()
        #genre_name='"'+genre_name+'"'
        #genre_code='"'+genre_code+'"'
        #genre_serial='"'+genre_serial+'"'

        sql_command="INSERT INTO genre(genre_id,genre,genre_code,genre_serial) VALUES(?,?,?,?)" 
        params=(genre_id,genre_name,genre_code,genre_serial)
        cursor.execute(sql_command,params)


    #Book vs genre table
    for index, row in df.iterrows():
        book_id=row['book_id']
        genre_id=row['genre_id']
        sql_command="INSERT INTO book_genre(book_id,genre_id) VALUES(?,?)" 
        params=(book_id,genre_id)
        cursor.execute(sql_command,params)
        
    #Book vs writer table
    for index, row in df.iterrows():
        book_id=row['book_id']
        auth_id=row['auth_id']
        sql_command="INSERT INTO book_writer(book_id,writer_id) VALUES(?,?)" 
        params=(book_id,auth_id)
        cursor.execute(sql_command,params)
    
    #Book vs year table
    for index, row in df.iterrows():
        book_id=row['book_id']
        year_id=row['year_id']
        sql_command="INSERT INTO book_year(book_id,year_id) VALUES(?,?)" 
        params=(book_id,year_id)
        cursor.execute(sql_command,params)

    #Book vs year table
    for index, row in df.iterrows():
        book_id=row['book_id']
        ed_id=row['ed_id']
        sql_command="INSERT INTO book_ed(book_id,ed_id) VALUES(?,?)" 
        params=(book_id,ed_id)
        cursor.execute(sql_command,params)
   
    db.commit()

  


    cursor.execute("SELECT * FROM books")
    records = cursor.fetchall()

    ## Showing the data
    for record in records:
        print(record)
    cursor.close()
    db.close()
