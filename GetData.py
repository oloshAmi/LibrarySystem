import wx
from wx.lib.intctrl import IntCtrl
from wx.adv import NotificationMessage
import sqlite3
from sqlite3 import Error
from ClassRecords import *
from HelperFunctions import *
import UIpanelRep

class GetData(wx.Dialog):
    def __init__(self,db, parent,result=None,title='None'):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title,size=(800,800))
        self.parent=parent
        self.db=db
        self.oldResult=result
        self.genre_info=get_genre_info(self.db)
        if(isinstance(parent, UIpanelRep.ResultPanel)):
            self.panel=UIpanelRep.EditPanel(self,wx.ID_ANY,self.db,self.oldResult)
        else:
            self.panel=UIpanelRep.InputPanel(self,wx.ID_ANY,self.genre_info)

        self.panel.saveButton.Bind(wx.EVT_BUTTON, self.SaveConnString)
        self.panel.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.Show()

    def OnQuit(self, event):
        self.result_name = None
        self.Destroy()

    def SaveConnString(self, event):
        #TODO: Perform all sorts of error check here. , show a successfully added screen
        self.genre = self.panel.cb_book_genre.GetValue()
        self.genre_code = self.panel.tc_genre_code.GetValue()
        self.genre_serial = self.panel.tc_genre_serial.GetValue()
        self.book_name = self.panel.tc_book_name.GetValue()
        self.writer_name = self.panel.tc_writer_name.GetValue()
        self.edition = self.panel.tc_book_edition.GetValue()
        #Year is forced to be int using IntCtrl()
        self.publ_year = self.panel.tc_publ_year.GetValue()
        if(isinstance(self.parent, UIpanelRep.ResultPanel)):
            self.book_serial=self.panel.tc_book_serial.GetValue()
            #deleteFromDB(self.db,self.oldResult[4])
            #TODO: write function to edit db rather than delete and add
            #addEntryToDB(self.db,self.genre_info,self.genre,self.genre_code,self.genre_serial, self.book_name,self.writer_name,self.edition,self.publ_year,book_serial=self.oldResult[3])
            self.resp=editDbEntry(self.db,self.genre_info,self.genre,self.genre_code,self.genre_serial,self.book_serial, self.book_name,self.writer_name,self.edition,self.publ_year,self.oldResult,self)

            if(self.resp):
               #ensures searchpanel, i.e. caller of the parent catches search specific event again, thus re-searching the db and posting new result! (Smart)
                evt = wx.CommandEvent()
                evt.SetEventType(wx.EVT_BUTTON.typeId)
                wx.PostEvent(self.parent.caller.searchButton, evt)

                self.nm=NotificationMessage(title='',message='Book Edited successfully',parent=self)
                self.nm.Show(timeout=wx.adv.NotificationMessage.Timeout_Auto)
            self.Destroy()        
        else:
            addEntryToDB(self.db,self.genre_info,self.genre,self.genre_code,self.genre_serial, self.book_name,self.writer_name,self.edition,self.publ_year)
            self.nm=NotificationMessage(title='',message='Book added successfully',parent=self)
            self.nm.Show(timeout=wx.adv.NotificationMessage.Timeout_Auto)
            self.Destroy()        
        
        #print(self.genre,self.genre_code,self.genre_serial, self.book_name,self.writer_name,self.edition,self.publ_year)

