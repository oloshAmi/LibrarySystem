import wx
from wx.lib.intctrl import IntCtrl
from wx.adv import NotificationMessage
import sqlite3
from sqlite3 import Error
from ClassRecords import *
from HelperFunctions import *
import LibrarySystem
#import Library_sqlite

from pubsub import pub
import  wx.lib.mixins.listctrl  as  listmix




class InputPanel(wx.Panel):
     def __init__(self, parent,id,genre_info):
        super().__init__(parent,id)
        
        self.gen_name_list=list()
        for gen_inf in genre_info:
            self.gen_name_list.append(gen_inf.genre)

        #controls the Panel
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        #Controls the below boxes of the panel
        self.sizer = wx.GridBagSizer(5,6)
        #Below section used to be a list with loops, but for reasons.... :P
        self.book_name=wx.StaticText(self, label="Book Name")
        self.tc_book_name=wx.TextCtrl(self)
        self.writer_name=wx.StaticText(self, label="Writer Name")
        self.tc_writer_name=wx.TextCtrl(self)
        self.book_genre=wx.StaticText(self, label="Book Genre")
        self.cb_book_genre=wx.ComboBox(self,choices=self.gen_name_list,style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER)
        self.genre_code=wx.StaticText(self, label="Genre Code")
        self.tc_genre_code=wx.TextCtrl(self)
        self.genre_serial=wx.StaticText(self, label="Genre Serial")
        self.tc_genre_serial=wx.TextCtrl(self)
        self.book_edition=wx.StaticText(self, label="Book Edition")
        self.tc_book_edition=wx.TextCtrl(self)
        self.publ_year=wx.StaticText(self, label="Publication Year")
        self.tc_publ_year=IntCtrl(self)

        self.sizer.Add(self.book_name, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.tc_book_name, pos=(0, 1),span=(1, 5), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=8)
        self.sizer.Add(self.writer_name, pos=(1, 0), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.tc_writer_name, pos=(1, 1),span=(1, 5), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=8)
        self.sizer.Add(self.book_genre, pos=(2, 0), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.cb_book_genre, pos=(2, 1), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.genre_code, pos=(2, 2), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.tc_genre_code, pos=(2, 3), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.genre_serial, pos=(2, 4), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.tc_genre_serial, pos=(2, 5), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(wx.StaticText(self), pos=(3, 0), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(wx.StaticText(self), pos=(3, 1), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.book_edition, pos=(3, 2), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.tc_book_edition, pos=(3, 3), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.publ_year, pos=(3, 4), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.tc_publ_year, pos=(3, 5), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
       
        self.saveButton =wx.Button(self, label="Save")
        self.sizer.Add(self.saveButton, pos=(5, 0), flag=wx.TOP|wx.LEFT,border=15)
        self.closeButton =wx.Button(self, label="Cancel")
        self.sizer.Add(self.closeButton, pos=(5, 1),flag=wx.TOP|wx.LEFT, border=15)

        self.hbox.Add(self.sizer, proportion=1, flag=wx.ALL|wx.EXPAND, border=0)
        self.SetSizer(self.hbox)

        self.cb_book_genre.Bind(wx.EVT_COMBOBOX,self.setOtherBoxProp)
        self.cb_book_genre.Bind(wx.EVT_TEXT_ENTER,self.reSetOtherBoxProp)
        
     def setOtherBoxProp(self,e):
            self.tc_genre_code.SetEditable(False)
            self.tc_genre_serial.SetEditable(False)
     def reSetOtherBoxProp(self,e):
            self.tc_genre_code.SetEditable(True)
            self.tc_genre_serial.SetEditable(True)
        

class EditPanel(wx.Panel):
    def __init__(self, parent,id,db,result):
        super().__init__(parent,id)
        self.db=db
        self.genre_info=get_genre_info(self.db)
        self.gen_name_list=list()
        for gen_inf in self.genre_info:
            self.gen_name_list.append(gen_inf.genre)

        #controls the Panel
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        #Controls the below boxes of the panel
        self.sizer = wx.GridBagSizer(5,6)
        #Below section used to be a list with loops, but for reasons.... :P
        self.book_name=wx.StaticText(self, label="Book Name")
        self.tc_book_name=wx.TextCtrl(self,value=result[4])
        self.writer_name=wx.StaticText(self, label="Writer Name")
        self.tc_writer_name=wx.TextCtrl(self,value=result[5])
        self.book_genre=wx.StaticText(self, label="Book Genre")
        self.cb_book_genre=wx.ComboBox(self,choices=self.gen_name_list,value=result[0],style=wx.CB_DROPDOWN)
        self.genre_code=wx.StaticText(self, label="Genre Code")
        self.tc_genre_code=wx.TextCtrl(self,value=result[1],style=wx.TE_READONLY)
        self.genre_serial=wx.StaticText(self, label="Genre Serial")
        self.tc_genre_serial=wx.TextCtrl(self,value=result[2],style=wx.TE_READONLY)
        self.book_serial=wx.StaticText(self, label="Book Serial")
        self.tc_book_serial=wx.TextCtrl(self,value=result[3])
        self.book_edition=wx.StaticText(self, label="Book Edition")
        self.tc_book_edition=wx.TextCtrl(self,value=result[6])
        self.publ_year=wx.StaticText(self, label="Publication Year")
        self.tc_publ_year=IntCtrl(self,value=result[7])

        self.sizer.Add(self.book_name, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.tc_book_name, pos=(0, 1),span=(1, 5), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=8)
        self.sizer.Add(self.writer_name, pos=(1, 0), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.tc_writer_name, pos=(1, 1),span=(1, 5), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=8)
        self.sizer.Add(self.book_genre, pos=(2, 0), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.cb_book_genre, pos=(2, 1), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.genre_code, pos=(2, 2), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.tc_genre_code, pos=(2, 3), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.genre_serial, pos=(2, 4), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.tc_genre_serial, pos=(2, 5), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.book_serial, pos=(3, 0), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.tc_book_serial, pos=(3, 1), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.book_edition, pos=(3, 2), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.tc_book_edition, pos=(3, 3), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.publ_year, pos=(3, 4), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.tc_publ_year, pos=(3, 5), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
       
        self.cb_book_genre.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.updateGenreList)

        self.saveButton =wx.Button(self, label="Save")
        self.sizer.Add(self.saveButton, pos=(5, 0), flag=wx.TOP|wx.LEFT,border=15)
        self.closeButton =wx.Button(self, label="Cancel")
        self.sizer.Add(self.closeButton, pos=(5, 1),flag=wx.TOP|wx.LEFT, border=15)

        self.hbox.Add(self.sizer, proportion=1, flag=wx.ALL|wx.EXPAND, border=0)
        self.SetSizer(self.hbox)
    
    def updateGenreList(self,e):
        self.genre_info=get_genre_info(self.db)
        self.gen_name_list=list()
        #Aesthetic purpose
        self.gen_name_list.append('')
        for gen_inf in self.genre_info:
            self.gen_name_list.append(gen_inf.genre)
        
        self.cb_book_genre.SetItems(self.gen_name_list)



class MainPanel(wx.Panel):
     def __init__(self, parent, db):
        super().__init__(parent)
        self.db=db
        self.BackgroundColour = (255, 255, 230)
        self.resultPanelBase = ResultPanelBase(self.db,parent=self)
        self.searchPanel = SearchPanel(self.db,self.resultPanelBase,parent=self)

        self.vertSizer = wx.BoxSizer( wx.VERTICAL )
        self.vertSizer.Add(self.searchPanel,  proportion=1, flag=wx.EXPAND )
        self.vertSizer.Add(self.resultPanelBase,  proportion=3, flag=wx.EXPAND )
        
        self.SetSizer(self.vertSizer)
        self.Layout()



class SearchPanel(wx.Panel):
    def __init__(self,db,resultPanelBase, parent):
        super().__init__(parent)
        self.resultPanelBase=resultPanelBase
        self.BackgroundColour = (100, 130, 150)
        self.db=db
        
        self.genre_info=get_genre_info(self.db)
        self.gen_name_list=list()
        #Aesthetic purpose
        self.gen_name_list.append('')
        for gen_inf in self.genre_info:
            self.gen_name_list.append(gen_inf.genre)


        #controls the Panel
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        #Controls the below boxes of the panel
        self.sizer = wx.GridBagSizer(4,6)

        self.book_name=wx.StaticText(self, label="Book Name")
        self.tc_book_name=wx.TextCtrl(self,style=wx.TE_PROCESS_ENTER)
        self.writer_name=wx.StaticText(self, label="Writer Name")
        self.tc_writer_name=wx.TextCtrl(self,style=wx.TE_PROCESS_ENTER)
        self.book_genre=wx.StaticText(self, label="Book Genre")
        self.cb_book_genre=wx.ComboBox(self,choices=self.gen_name_list,style=wx.CB_READONLY)
        

        self.sizer.Add(self.book_name, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.tc_book_name, pos=(0, 1),span=(1, 5), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=8)
        self.sizer.Add(self.writer_name, pos=(1, 0), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.tc_writer_name, pos=(1, 1),span=(1, 5), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=8)
        self.sizer.Add(self.book_genre, pos=(2, 0), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        self.sizer.Add(self.cb_book_genre, pos=(2, 1), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
       
        self.searchButton =wx.Button(self, label="Search")
        self.sizer.Add(self.searchButton, pos=(4, 4), flag=wx.LEFT|wx.BOTTOM,border=15)
        self.searchAllButton =wx.Button(self, label="Search All")
        self.sizer.Add(self.searchAllButton, pos=(4, 5),flag=wx.LEFT|wx.BOTTOM, border=15)

        self.hbox.Add(self.sizer, proportion=1, flag=wx.ALL|wx.EXPAND, border=0)
        self.SetSizer(self.hbox)

        #below event ensures fresh list is displayed in the combobox
        self.cb_book_genre.Bind(wx.EVT_COMBOBOX_DROPDOWN,self.updateGenreList)

        self.searchButton.Bind(wx.EVT_BUTTON, self.searchSpecificValue)
        self.searchAllButton.Bind(wx.EVT_BUTTON, self.searchAllValues)
        self.tc_book_name.Bind(wx.EVT_TEXT_ENTER, self.onEnter)
        self.tc_writer_name.Bind(wx.EVT_TEXT_ENTER, self.onEnter)
    
    def updateGenreList(self,e):
        self.genre_info=get_genre_info(self.db)
        self.gen_name_list=list()
        #Aesthetic purpose
        self.gen_name_list.append('')
        for gen_inf in self.genre_info:
            self.gen_name_list.append(gen_inf.genre)
        
        self.cb_book_genre.SetItems(self.gen_name_list)

    def onEnter(self,event):
         self.searchSpecificValue(event)
     
    def searchSpecificValue(self,event):
        self.genre = self.cb_book_genre.GetValue()
        self.book_name = self.tc_book_name.GetValue()
        self.writer_name = self.tc_writer_name.GetValue()
        self.results=searchSpecificEntryFromDB(self.db,self.genre,self.book_name,self.writer_name)
        self.setupResultPanel()

    def searchAllValues(self,event):
        self.results=searchAllEntryFromDB(self.db)
        self.setupResultPanel()

    def setupResultPanel(self):
        #Pubsub is a message based system for multithreding, counter is a class variable, If this is not the first instance of the
        # ResultPanel class, then remove the existing listctrl
        if(ResultPanel.counter!=0):
            pub.sendMessage('UpdateListview')
        self.resultPanel = ResultPanel(self.results,self.db,self,parent=self.resultPanelBase)



class ResultPanel(wx.Panel):
    counter = 0
    def __init__(self,results,db,caller,parent):        
        super().__init__(parent)
        self.db=db
        self.caller=caller
        ResultPanel.counter += 1
        self.results=results
        self.publishResult()    
        self.BackgroundColour = (200, 230, 250)
        parent.sizer = wx.BoxSizer(wx.HORIZONTAL)
        parent.sizer.Add(self, proportion=1, flag=wx.ALL|wx.EXPAND, border=0)
        parent.SetSizer(parent.sizer)
        parent.Layout()

    def publishResult(self):
        #self.list_ctrl=wx.ListCtrl(self, style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.list_ctrl=TestListCtrl(self,ID=wx.ID_ANY, style=wx.LC_REPORT|wx.BORDER_SUNKEN)   
        #subscribe is from pubsub, ¨the current instance of the object is listed there,
        # when updatelistview is called from another class, it'll execute the function
        #https://stackoverflow.com/questions/46818117/how-to-delete-items-on-wx-listctrl-from-another-frame
        pub.subscribe(self.UpdateListView, 'UpdateListview')
        #self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)        
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)

        self.list_ctrl.InsertColumn(0, 'Genre')
        self.list_ctrl.InsertColumn(1, 'Genre Code')
        self.list_ctrl.InsertColumn(2, 'Genre Serial', width=125)
        self.list_ctrl.InsertColumn(3, 'Book Serial', width=125)
        self.list_ctrl.InsertColumn(4, 'Book Name', width=300)
        self.list_ctrl.InsertColumn(5, 'Author', width=300)
        self.list_ctrl.InsertColumn(6, 'Edition', width=125)
        self.list_ctrl.InsertColumn(7, 'Published Year', width=125)

        index = 0
        for data in self.results:
            self.list_ctrl.InsertItem(index, data[0])
            self.list_ctrl.SetItem(index, 1, data[1])
            self.list_ctrl.SetItem(index, 2, data[2])
            self.list_ctrl.SetItem(index, 3, data[3])
            self.list_ctrl.SetItem(index, 4, data[4])
            self.list_ctrl.SetItem(index, 5, data[5])
            self.list_ctrl.SetItem(index, 6, data[6])
            self.list_ctrl.SetItem(index, 7, str(data[7]))
            index += 1

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.list_ctrl, proportion=1, flag=wx.ALL|wx.EXPAND, border=0)
        self.SetSizer(self.sizer)
    def UpdateListView(self):
        self.Destroy()

    def onRightClick(self,event):    
        self.currentItemID=event.GetItem().GetId()
        menu = wx.Menu()
        # add some items
        menu.Append(wx.ID_DELETE, "Delete")
        menu.Append(wx.ID_EDIT, "Edit")
        menu.Append(wx.ID_ANY, "Cancel")
        self.PopupMenu(menu)
        self.Bind(wx.EVT_MENU,self.deleteItem,id=wx.ID_DELETE)
        self.Bind(wx.EVT_MENU,self.editItem,id=wx.ID_EDIT)
        

    def deleteItem(self,event):

        resp=deleteFromDB(self.db,self.results[self.currentItemID][4])
        if(resp==1):
            self.nm=NotificationMessage(title='',message='Book Deleted successfully',parent=self)
            self.nm.Show(timeout=wx.adv.NotificationMessage.Timeout_Auto)
            #ensures searchpanel, i.e. caller catches search specific event again, thus re-searching the db and posting new result! (Smart)
            evt = wx.CommandEvent()
            evt.SetEventType(wx.EVT_BUTTON.typeId)
            wx.PostEvent(self.caller.searchButton, evt)

        else:
            self.nm=NotificationMessage(title='',message='Deletion Error',parent=self)
            self.nm.Show(timeout=wx.adv.NotificationMessage.Timeout_Auto)
    
    def editItem(self,event):
        
       # print(self.results[self.currentItemID])
        dlg = LibrarySystem.GetData(self.db,parent = self,result=self.results[self.currentItemID],title='Edit Entry') 
       


class TestListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)

class ResultPanelBase(wx.Panel):
    def __init__(self,db,parent):
        super().__init__(parent)    
        self.BackgroundColour = (200, 230, 250)
