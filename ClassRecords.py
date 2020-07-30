class Book:
    def __init__(self,book_name='',book_serial='',book_ed='Unknown Edition', publ_year=0,writer='Unknown Author'):
        self.book_serial=book_serial
        self.book_name=book_name
        self.book_ed=book_ed
        self.publ_year=publ_year
        self.writer=writer

class Genre:
    def __init__(self,genre='Unknown', genre_code='',genre_serial='',new_genre=False):
        self.genre=genre
        self.genre_code=genre_code
        self.genre_serial=genre_serial
        self.new_genre=new_genre

class DbEntry:
    def __init__(self,genre=Genre(),book=Book()):
        self.genre=genre
        self.book=book