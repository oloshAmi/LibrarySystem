def loadFromExcel(conn):    
    import pandas as pd
    from putDataInDB import put_data_in_db


    #Initialize
    file_name='Library Index.xlsx'

    #Read the excel file in a dictionary
    sheet_to_df_map = pd.read_excel(file_name, sheet_name=None)

    for key in sheet_to_df_map.keys():
        if key=='Index':
            dict_idx=sheet_to_df_map.pop(key)
            break


    temp=list()
    dic_key=list(sheet_to_df_map.keys())
    for key in dic_key:
        temp.append(sheet_to_df_map.pop(key))

    #Create dataframe, didn't find more elegant solution, handle nulls and repeatation of column names
    df=pd.concat([pd.DataFrame(temp[i]) for i in range(len(temp))],ignore_index=True)
    df.rename(columns={'Sl.No.': 'serial_num'}, inplace=True)
    #Drop rows where the column headers were duplicated in excel
    df=df[~df.Edition.str.contains("Edition",na=False)]
    #Drop rows where all columns (except) serial number is null / Corresponds to empty cells in excel
    df.dropna(how='all',subset=['Name', 'Author','Edition','Year'],inplace=True)
    df['Author'] = df['Author'].fillna('Unknown Author')
    df['Edition'] = df['Edition'].fillna('Unknown Edition')
    df['Year'] = df['Year'].fillna(0000)
    df['serial_num'] = df['serial_num'].astype("string").str.lower().str.strip()
    df['Name'] = df['Name'].astype("string").str.lower().str.strip()
    df['Author'] = df['Author'].astype("string").str.lower().str.strip()
    df['Edition'] = df['Edition'].astype("string").str.lower().str.strip()
    df['Year'] = df['Year'].astype("int64")
    df['book_id']=[i for i in range(df['Year'].size)]    
    df['auth_id']=mapped_id(df,'Author')
    df['ed_id']=mapped_id(df,'Edition')
    df['year_id']=mapped_id(df,'Year')
    
    genre=pd.DataFrame(dict_idx)
    genre= genre.fillna('Not Available')
    genre['Genre'] = genre['Genre'].astype("string").str.lower().str.strip()
    genre['Genre_code'] = genre['Genre_code'].astype("string").str.lower().str.strip()
    gen=list(genre['Genre_serial'])
    for i in range(len(gen)):
        gen[i]=str(gen[i])
    genre['Genre_serial'] =gen
    genre['Genre_serial'] = genre['Genre_serial'].astype("string").str.lower().str.strip()
    genre['Genre_id']=[i for i in range(genre['Genre'].size)]    

    book_ser=list(df['serial_num'])
    book_ser_id=book_ser.copy()
    for i in range(len(gen)):
        index_pos_list = [j for j in range(len(book_ser)) if gen[i] in book_ser[j]]
        for k in range(len(index_pos_list)):
            book_ser_id[index_pos_list[k]]=i



    df['genre_id']=book_ser_id


    genre['Genre_id']= genre['Genre_id']+1
    df['book_id']=df['book_id']+1
    df['auth_id']=df['auth_id']+1
    df['ed_id']=df['ed_id']+1
    df['year_id']=df['year_id']+1
    df['genre_id']=df['genre_id']+1

    print(df.info())
    db_con=conn
    put_data_in_db(db_con,df,genre)





def mapped_id(df,col_name):
    un_col=unique_col_val(df,col_name)
    col_list=list(df[col_name])
    col_id=col_list.copy()
    
    #Crap code
    for i in range(len(un_col)):
        index_pos_list = [ j for j in range(len(col_list)) if col_list[j] == un_col[i] ]
        for k in range(len(index_pos_list)):
            col_id[index_pos_list[k]]=i

    return col_id

def unique_col_val(df,col_name):
    col=list(df[col_name])
    un_col=list(set(col))
    return un_col



