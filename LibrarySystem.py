import os
import sqlite3
from sqlite3 import Error
#from create_db_and_tables import *


import wx
from wx.lib.intctrl import IntCtrl
from wx.adv import NotificationMessage
import mysql.connector as mysql
from ClassRecords import *
from HelperFunctions import *
from UIpanelRep import *
#from LoadFromExcel import *
from GetData import GetData

APP_EXIT = 1

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cws=os.getcwd()
        self.db_file=self.cws+"\Database\personal_library.db"
        self.InitDB()
        self.InitUI()
        self.SetTitle('Taleb Ali Memorial Library')
        self.Centre()
        self.Maximize()
    
    def InitDB(self):
        self.db=create_connection(self.db_file)
        #self.genre_info=get_genre_info(self.db)


    def OnQuit(self,e):
        self.Close()

    def getInput(self,event):
            dlg = GetData(self.db,parent = self,title='Add Data') 
            dlg.ShowModal()
            dlg.Destroy()


    def InitUI(self):
        menuBar=MainMenuBar()       
        self.Bind(wx.EVT_MENU,self.OnQuit,id=APP_EXIT)
        self.Bind(wx.EVT_MENU,self.getInput,id=wx.ID_ADD)
        self.SetMenuBar(menuBar)
        self.mainPanel = MainPanel(self,self.db)


class MainMenuBar(wx.MenuBar):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fileMenu=wx.Menu()
        self.qmi=wx.MenuItem(self.fileMenu,APP_EXIT,'&Quit\tCTRL+Q')
        self.fileMenu.Append(self.qmi)
        self.Append(self.fileMenu,'&File')

        self.addItemMenu=wx.Menu()
        self.addmi=wx.MenuItem(self.addItemMenu,wx.ID_ADD)
        self.addItemMenu.Append(self.addmi)
        self.Append(self.addItemMenu,'&Add Book')

        
     



def main():
    app = wx.App()
    ex = MainFrame(None)
    ex.Show()
    app.MainLoop()

    #To create new db, uncomment the below line and create_stuff() function, uncomment #from create_db_and_tables import *, and comment from HelperFunctions import *
    #To load from excel into that db, comment the create_stuff() and import and uncomment loadFromExcel() and #from LoadFromExcel import *, and uncomment from HelperFunctions import *
    #cws=os.getcwd()
    #database = cws+"\Database\personal_library.db"

    #conn=create_connection(database)
    #create_stuff(database)
    #loadFromExcel(conn)
    
   


        
if __name__ == '__main__':
    main()
