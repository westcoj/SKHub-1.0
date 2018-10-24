'''
Created on Sep 25, 2018

@author: Cody
'''

import wx
import wx.media
import os
import wx.lib.buttons as buttons
from SKClient import SKClient
from SKMedia import SKMedia
from SKFile import SKFile
import configparser
import ipaddress


dirName = os.path.dirname(os.path.realpath(__file__))
#HAS TO BE CHANGED LATER
bitmapDir = os.path.join(dirName,'bitmaps')
class SKGUI(wx.Panel):
    '''
    Class meant to build and operate the GUI. Due to MediaCTRL's operation
    the media player functions are wrapped in the GUI. This means that a
    command line only client isn't possible.
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        wx.Panel.__init__(self,parent=parent)
        self.mediaManager = SKMedia()
        self.frame = parent
        self.currentVolume = 50
        self.createMenu()
#         self.skSetConnection(wx.EVT_CATEGORY_ALL)
        self.skc = self.skStartup() #SKClient("C:\\SoundFiles\\Client\\", 1445, '127.0.0.1')
        self.createLayout()
        
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.onTimer)
        self.timer.Start(100)
        self.listDisplay = ''
        self.playIndex = 0
        
    def skStartup(self):
        '''
        Method for either running setup wizard, or grabbing information from ini file.
        Returns a created SKClient to use for connections.
        '''
        
        dirName = os.path.dirname(os.path.realpath(__file__))
        if(os.path.isfile('sksettings.ini')):
            #Process ini file
            try:
                config = configparser.ConfigParser()
                config.read('sksettings.ini')
                self.__host = config['DEFAULT']['ServerIP']
                self.__port = int(config['DEFAULT']['ServerPort'])
                self.__pass = config['DEFAULT']['ConnectionPassword']
                self.__admPass = config['DEFAULT']['AdminPassword']
                self.__path = config['DEFAULT']['ClientDirectory']
                return SKClient(self.__path, self.__port, self.__host)
            except Exception as e:
                print(e)
                defPath = os.path.join(dirName,'Music')
                return SKClient(defPath, 1445, 'NOIP')

        else:
            wx.MessageBox("Unable to load ini file, running start up.","ERROR",wx.ICON_EXCLAMATION|wx.OK)
            while True:
                while True:
                    '''Get IP'''
                    self.__host = self.skPopUpValue('Enter Server IP', '127.0.0.1')
                    try:
                        ipaddress.ip_address(self.__host)
                        break
                    except:
                        wx.MessageBox("Enter a valid IP address","ERROR",wx.ICON_EXCLAMATION|wx.OK)
                while True:
                    '''Get Port'''
                    try:
                        self.__port = int(self.skPopUpValue('Enter Server Port', '65535'))
                        break
                    except:
                        wx.MessageBox("Enter a valid port","ERROR",wx.ICON_EXCLAMATION|wx.OK)
                self.__path = self.skPopUpValue('Enter Download Directory', os.path.join(dirName,'Music'))
                try:
                    if not self.__path.endswith('\\'):
                        self.__path = self.__path + '\\'
                    if not os.path.isdir(self.__path):
                        os.makedirs(self.__path)
                except:
                    pass
                self.__pass = self.skPopUpValue('Connection Password', '')
                self.__admPass = self.skPopUpValue('Enter Admin Password (if known)', '')
                try:
                    config = configparser.ConfigParser()
                    config['DEFAULT'] = {}
                    config['DEFAULT']['ServerIP'] = self.__host
                    config['DEFAULT']['ServerPort'] = str(self.__port)
                    config['DEFAULT']['ConnectionPassword'] = self.__pass
                    config['DEFAULT']['AdminPassword'] = self.__admPass
                    config['DEFAULT']['ClientDirectory'] = self.__path
                    with open('sksettings.ini', 'w') as iniFile:
                        config.write(iniFile)
                except Exception as e:
                    print(e)
                    print('Error making ini file')
                return SKClient(self.__path, self.__port, self.__host)

    def skPopUpValue(self, text, defValue):
        '''
        Method that generates a pop up dialog box for errors
        '''
        popup = wx.TextEntryDialog(None, text, value = defValue)
        popup.ShowModal()
        value = popup.GetValue()
        popup.Destroy()
        return value
    
    def skTestServer(self):
        '''
        Later Method for making sure there is a valid connection
        '''
        check = self.skc.skOpen()
        if(check == 0):
            self.skc.skClose()
            return True
        else:
            return False
                    
    def createLayout(self):
        '''
        Create layout of GUI
        '''
        try:
            self.mediaPlayer = wx.media.MediaCtrl(self,style=wx.SIMPLE_BORDER, szBackend=wx.media.MEDIABACKEND_WMP10)
            self.Bind(wx.media.EVT_MEDIA_LOADED,self.loadPlay)
            self.mediaPlayer.Bind(wx.media.EVT_MEDIA_FINISHED, self.onNext, self.mediaPlayer)

        except:
            self.Destroy()
            
        self.playSlider = wx.Slider(self, size=wx.DefaultSize)
        self.Bind(wx.EVT_SLIDER,self.onSeek,self.playSlider)

        
        self.volumeCOP = wx.Slider(self, style=wx.SL_VERTICAL|wx.SL_INVERSE)
        self.volumeCOP.SetRange(0, 100)
        self.volumeCOP.SetValue(self.currentVolume)
        self.volumeCOP.Bind(wx.EVT_SLIDER, self.onSetVolume)
        
#         self.mediaDisplay = wx.ListBox(self, size=wx.DefaultSize, choices = [],style=wx.LB_SINGLE)
        self.mediaDisplay = wx.ListCtrl(self, size=(-1,450), style = wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self.mediaDisplay.InsertColumn(0 ,'Song',width = 150)
        self.mediaDisplay.InsertColumn(1 ,'Artist',width = 150)
        self.mediaDisplay.InsertColumn(2 ,'Album',width = 150)

#         self.mediaList = self.mediaManager.skMediaGetList()
        
        self.mediaList = []
        i=0
        for x in self.skc.skGetDir():
            self.mediaList.append(x)
            self.mediaDisplay.Append([x.title,x.artist,x.album])
            self.mediaDisplay.SetItemData(i, int(x.index))
            i+=1

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.skGetFile, self.mediaDisplay)


        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        audioSizer = self.buildAudioBar()
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
 
        # layout widgets
        mainSizer.Add(self.playSlider, 1, wx.ALL|wx.EXPAND, 5)
        hSizer.Add(audioSizer, 0, wx.ALL|wx.CENTER, 5)
        hSizer.Add(self.volumeCOP, 0, wx.ALL, 5)
        mainSizer.Add(hSizer)
        topSizer.Add(mainSizer)
        topSizer.Add(self.mediaDisplay,1,wx.RIGHT|wx.EXPAND,5)

        self.SetSizer(topSizer)
        self.Layout()
 
    def buildAudioBar(self):
        """
        Builds the audio bar controls
        """
        audioBarSizer = wx.BoxSizer(wx.HORIZONTAL)
 
        self.buildBtn({'bitmap':'prev.png', 'handler':self.onPrev,
                       'name':'prev'},
                      audioBarSizer)
 
        # create play/pause toggle button
        img = wx.Bitmap(os.path.join(bitmapDir, "play.png"))
        self.playPauseBtn = buttons.GenBitmapToggleButton(self, bitmap=img, name="play")
        self.playPauseBtn.Enable(False)
 
        img = wx.Bitmap(os.path.join(bitmapDir, "pause.png"))
        self.playPauseBtn.SetBitmapSelected(img)
        self.playPauseBtn.SetInitialSize()
 
        self.playPauseBtn.Bind(wx.EVT_BUTTON, self.onPlay)
        audioBarSizer.Add(self.playPauseBtn, 0, wx.LEFT, 3)
 
        btnData = [{'bitmap':'stop.png',
                    'handler':self.onStop, 'name':'stop'},
                    {'bitmap':'next.png',
                     'handler':self.onNext, 'name':'next'}]
        for btn in btnData:
            self.buildBtn(btn, audioBarSizer)
 
        return audioBarSizer
 
    def buildBtn(self, btnDict, sizer):
        """"""
        bmp = btnDict['bitmap']
        handler = btnDict['handler']
 
        img = wx.Bitmap(os.path.join(bitmapDir, bmp))
        btn = buttons.GenBitmapButton(self, bitmap=img, name=btnDict['name'])
        btn.SetInitialSize()
        btn.Bind(wx.EVT_BUTTON, handler)
        sizer.Add(btn, 0, wx.LEFT, 3)
 
    def createMenu(self):
        """
        Creates a menu
        """
        menubar = wx.MenuBar()
 
        fileMenu = wx.Menu()
        conn_item = fileMenu.Append(wx.Window.NewControlId(), "&Connect","Connect to Server")
        menubar.Append(fileMenu, '&File')
        
        mediaMenu = wx.Menu()
        updateListItem = mediaMenu.Append(wx.Window.NewControlId(), "&Update", "Update Media Directory")
        listItem = mediaMenu.Append(wx.Window.NewControlId(), "&Playlists", "Create Playlist")
        shuffleItem = mediaMenu.Append(wx.Window.NewControlId(), '&Shuffle', 'Shuffle Current List')
        menubar.Append(mediaMenu, '&Media')
        
#         connection_menu = 
        self.frame.SetMenuBar(menubar)
        self.frame.Bind(wx.EVT_MENU, self.skSetConnection, conn_item)
        self.frame.Bind(wx.EVT_MENU, self.skGetList, updateListItem)
        self.frame.Bind(wx.EVT_MENU, self.skListOption, listItem)
        self.frame.Bind(wx.EVT_MENU, self.skShuffleList, shuffleItem)

    def skSetConnection(self,event):
        self.skc = SKClient("C:\\SoundFiles\\Client\\", 1445, '127.0.0.1')#'192.168.0.183');
        self.connected = self.skc.skOpen()
        self.skc.skClose()
        

    def skGetList(self, event):
        '''
        Method for updating default display list
        '''
        self.skc.comSwitch('update')
        self.mediaList = []
        self.mediaDisplay.DeleteAllItems()
        i = 0
        for x in self.skc.skGetDir():
                self.mediaList.append(x)
                self.mediaDisplay.Append([x.title,x.artist,x.album])
                self.mediaDisplay.SetItemData(i, int(x.index))
                i+=1
        check = self.mediaManager.skdbUpdateDefault(self.mediaList)
        
    def skListOption(self, event):
        '''
        Method for opening list management GUI
        '''
        frame = SKListFrame(self.mediaManager, self)
        frame.Show()
        
    def skLoadList(self, event, name):
        '''
        Method that loads a play list from manager
        '''
#         self.mediaList = []
#         self.mediaDisplay.Clear()
#         if(name == 'Library'):
#             name = 'defPlaylist'
#         vals = self.mediaManager.skdbGetList(name)
#         for x in vals:
#                 self.mediaList.append(x)
#                 self.mediaDisplay.Append((x.artist.strip(' ') + ' : ' + x.title),x)
##########----------REPORT VERSION-----------------#

        self.mediaList = []
        self.mediaDisplay.DeleteAllItems()
        if(name == 'Library'):
            name = 'defPlaylist'
        i=0
        vals = self.mediaManager.skdbGetList(name)
        for x in vals:
            self.mediaList.append(x)
            self.mediaDisplay.Append([x.title,x.artist,x.album])
            self.mediaDisplay.SetItemData(i, int(x.index))
            i+=1
                
    def skShuffleList(self, event):
        '''
        Method that shuffles currently selected list
        '''
#         tempList = self.mediaManager.skShuffleList(self.mediaList)
#         self.mediaList = []
#         self.mediaDisplay.Clear()
#         for x in tempList:
#             self.mediaDisplay.Append((x.artist.strip(' ') + ' : ' + x.title),x)
#             self.mediaList.append(x)
#         self.mediaManager.skSetList(self.mediaList)
    ###-----------REPORT VERSION--------_#
        tempList = self.mediaManager.skShuffleList(self.mediaList)
        self.mediaList = []
        self.mediaDisplay.DeleteAllItems()
        i=0
        for x in tempList:
            self.mediaDisplay.Append([x.title,x.artist,x.album])
            self.mediaDisplay.SetItemData(i, int(x.index))
            self.mediaList.append(x)
            i+=1
#         self.mediaManager.skSetList(self.mediaList) OLD LIST USAGE
        
    def skGetFile(self, event):
        '''
        Method for downloading a music file, upon finishing download, play music
        '''
        #Get data of current box selection
#         skf = self.mediaDisplay.GetClientData(self.mediaDisplay.GetSelection())
#         indexSKF = self.mediaDisplay.GetItemData(self.mediaDisplay.GetFocusedItem())
        indexSKF = self.mediaDisplay.GetItemData(event.GetIndex())
        #Song's unique index
        self.playIndex = self.mediaDisplay.GetFocusedItem()#self.mediaDisplay.GetSelection()
        index = int(indexSKF) #int(skf.index)
        try:
            #Has a song been played yet, avoid attempted load of current song
            self.currentSong
        except AttributeError:
            cs = False
        else:
            cs = True 
        if(cs):
            #Start current song over again
            if(self.currentSong == index): #skf.index):
                self.loadMusic(self.skc.skGetPath() + self.skc.skGetDir()[index].path)
                return
        val = self.skc.skGUIFILE(index)
        if val == 1:
            #continue
            self.loadMusic(self.skc.skGetPath() + self.skc.skGetDir()[index].path)
            self.currentSong = index
        else:
            wx.MessageBox("Unable to load %s: No file found" % self.mediaList[index].title,"ERROR",wx.ICON_EXCLAMATION|wx.OK)
        
    def loadMusic(self, musicFile):
        """
        Load the music into the MediaCtrl or display an error dialog
        if the user tries to load an unsupported file type
        """
        if not self.mediaPlayer.Load(musicFile):
            wx.MessageBox("Unable to load %s: Unsupported format?" % musicFile,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mediaPlayer.SetInitialSize()
            self.GetSizer().Layout()
            self.playSlider.SetRange(0, self.mediaPlayer.Length())
            self.playPauseBtn.Enable(True)
 
 
    def onNext(self, event):
        """
        Not implemented!
        """ 
#         self.mediaPlayer.Stop()
#         #Stop if final song
#         if(self.playIndex == len(self.mediaList)-1):
#             self.onStop(wx.EVT_CATEGORY_ALL)
#             return
#         #Get song after current song, playIndex tracks index in the playlist, in case the selection is moved, 
#         #But a new song is not chosen.
#         skf = self.mediaDisplay.GetClientData(self.playIndex + 1)
#         index = int(skf.index)
#         val = self.skc.skGUIFILE(index)
#         if val == 1:
#             #continue
#             self.loadMusic(self.skc.skGetPath() + self.mediaList[self.playIndex + 1].path)
#             self.mediaDisplay.SetSelection(self.playIndex + 1)
#             self.currentSong=skf
#             self.playIndex+=1
#         else:
#             wx.MessageBox("Unable to load %s: No file found" % self.mediaList[index],"ERROR",wx.ICON_EXCLAMATION|wx.OK)
            
        ###--------REPORT VERSION-------###
        self.mediaPlayer.Stop()
        #Stop if final song
        if(self.playIndex == len(self.mediaList)-1):
            self.onStop(wx.EVT_CATEGORY_ALL)
            return
        #Get song after current song, playIndex tracks index in the playlist, in case the selection is moved, 
        #But a new song is not chosen.

        index = self.mediaDisplay.GetItemData(self.playIndex + 1)
        val = self.skc.skGUIFILE(index)
        if val == 1:
            #continue
            self.loadMusic(self.skc.skGetPath() + self.mediaList[self.playIndex + 1].path)
            self.mediaDisplay.Select(self.playIndex + 1, True)
            self.mediaDisplay.SetItemState(self.playIndex+1, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
            self.currentSong=index
            self.playIndex+=1
        else:
            wx.MessageBox("Unable to load %s: No file found" % self.mediaList[index],"ERROR",wx.ICON_EXCLAMATION|wx.OK)
 
    def onPause(self):
        self.mediaPlayer.Pause()
 
    def onPlay(self, event):
        """
        Plays the music
        """
        if not event.GetIsDown():
            self.onPause()
            return
 
        if not self.mediaPlayer.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mediaPlayer.SetInitialSize()
            self.GetSizer().Layout()
            self.playSlider.SetRange(0, self.mediaPlayer.Length())
 
        event.Skip()
        
    def loadPlay(self, event):
        '''
        Method that plays the loaded music automatically
        '''
        self.mediaPlayer.Play()
        self.mediaPlayer.SetInitialSize()
        self.GetSizer().Layout()
        self.playSlider.SetRange(0, self.mediaPlayer.Length())
        self.playPauseBtn.SetValue(True)
 
 
    def onPrev(self, event):
        """
        Method that loads up the previous song, based on playlist order.
        """
#         self.mediaPlayer.Stop()
#         if(self.playIndex == 0):
#             self.onStop(wx.EVT_CATEGORY_ALL)
#             return
#         skf = self.mediaDisplay.GetClientData(self.playIndex - 1)
#         index = int(skf.index)
#         val = self.skc.skGUIFILE(index)
# #         print(self.skc.skGetPath() + self.mediaList[index])
#         if val == 1:
#             #continue
#             self.loadMusic(self.skc.skGetPath() + skf.path)
#             self.mediaDisplay.SetSelection(self.playIndex - 1)
#             self.currentSong=skf
#             self.playIndex -= 1
#         else:
#             wx.MessageBox("Unable to load %s: No file found" % self.mediaList[index],"ERROR",wx.ICON_EXCLAMATION|wx.OK)
    ####------------REPORT VERSION--------------------###
        self.mediaPlayer.Stop()
        if(self.playIndex == 0):
            self.onStop(wx.EVT_CATEGORY_ALL)
            return
        index = self.mediaDisplay.GetItemData(self.playIndex - 1)
        val = self.skc.skGUIFILE(index)
#         print(self.skc.skGetPath() + self.mediaList[index])
        if val == 1:
            #continue
            self.loadMusic(self.skc.skGetPath() +  self.mediaList[self.playIndex - 1].path)
            self.mediaDisplay.Select(self.playIndex - 1, True)
            self.currentSong=index
            self.playIndex -= 1
        else:
            wx.MessageBox("Unable to load %s: No file found" % self.mediaList[index],"ERROR",wx.ICON_EXCLAMATION|wx.OK)
 
    def onSeek(self, event):
        """
        Seeks the media file according to the amount the slider has
        been adjusted. (Fix the weird lag on click, might be fixed with mPlayer)
        """
        offset = self.playSlider.GetValue()
        self.mediaPlayer.Seek(offset)
 
    def onSetVolume(self, event):
        """
        Sets the volume of the music player
        """
        self.currentVolume = self.volumeCOP.GetValue()
#         print "setting volume to: %s" % int(self.currentVolume)
        self.mediaPlayer.SetVolume(float(self.currentVolume/100))
 
    def onStop(self, event):
        """
        Stops the music and resets the play button
        """
        self.mediaPlayer.Stop()
        self.playPauseBtn.SetToggle(False)
 
    def onTimer(self, event):
        """
        Keeps the player slider updated
        """
        offset = self.mediaPlayer.Tell()
        self.playSlider.SetValue(offset)
 
########################################################################
class MediaFrame(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "SounderKin 0.1", size=(800,300))
        panel = SKGUI(self)
 
 
########################################################################
class SKListFrame(wx.Frame):
    '''
    Class for secondary GUI that manages playlist loading and creation
    '''
    def __init__(self, skm, parent):
        '''
        Gets passed the list of playlists?
        '''
        self.skm = skm
        wx.Frame.__init__(self,None,title='Playlist Management', size=(400,300))
        self.panel = wx.Panel(self)
        #Create List Display
        self.mediaDisplay = wx.ListBox(self.panel, size=(75,150),style=wx.LB_HSCROLL, choices = [])
        self.mediaDisplay.Bind(wx.EVT_LISTBOX_DCLICK, 
                               lambda event: parent.skLoadList(event, self.mediaDisplay.GetString(self.mediaDisplay.GetSelection())),
                                self.mediaDisplay)
        self.refresh()
        self.newBtn = wx.Button(self.panel,label='New Playlist')
        self.newBtn.Bind(wx.EVT_BUTTON,self.newList)
        self.editBtn = wx.Button(self.panel,label='Edit Playlist')
        self.editBtn.Bind(wx.EVT_BUTTON,self.editList)
        self.dlBtn = wx.Button(self.panel,label='Delete Playlist')
        self.dlBtn.Bind(wx.EVT_BUTTON,self.delList)
        
        font = wx.Font(12, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
        lbl1 = wx.StaticText(self.panel,-1,style=wx.ALIGN_CENTER)
        lbl1.SetFont(font)
        lbl1.SetLabel('Playlist')
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.newBtn,0,wx.ALL|wx.LEFT,5)
        btnSizer.Add(self.dlBtn,0,wx.ALL|wx.RIGHT,5)
        btnSizer.Add(self.editBtn,0,wx.ALL|wx.CENTER,5)
        
        sizer.Add(lbl1,0,wx.ALL,5)
        sizer.Add(self.mediaDisplay, 0,wx.ALL|wx.EXPAND,5)
        sizer.Add(btnSizer)
        self.panel.SetSizer(sizer)
        
    def newList(self,event):
        dlg = wx.TextEntryDialog(self,'Enter List Name', 'Name Playlist')
        dlg.SetValue('NewList')
        if dlg.ShowModal() == wx.ID_OK:
            print(dlg.GetValue())
            val = self.skm.skdbNewList(dlg.GetValue())
            if val == 0:
                ''' Error Report '''
                wx.MessageBox("Issue creating list","ERROR",wx.ICON_EXCLAMATION|wx.OK)

        dlg.Destroy()
        self.refresh()
        
    def delList(self, event):
        plName = self.mediaDisplay.GetString(self.mediaDisplay.GetSelection())
        print(plName)
        if(plName == 'Library'):
            wx.MessageBox("DONT DO THAT","ERROR",wx.ICON_EXCLAMATION|wx.OK)
            return
        self.skm.skdbRemoveList(plName)
        self.refresh()
        
    def refresh(self):
        self.mediaDisplay.Clear()
        for x in self.skm.skdbGetAll():
            if(x=='_defPlaylist_OLD'):
                pass
            elif(x=='defPlaylist'):
                self.mediaDisplay.Append('Library')
            else:
                self.mediaDisplay.Append(x)
                
    def editList(self, event):
        '''
        Method that allows more mass editing of playlists
        
        Will require yet another frame
        '''
        if(self.mediaDisplay.GetString(self.mediaDisplay.GetSelection())=='Library'):
            wx.MessageBox("DONT DO THAT","ERROR",wx.ICON_EXCLAMATION|wx.OK)
            return
        secondFrame = SKEditFrame(self.skm, self.mediaDisplay.GetString(self.mediaDisplay.GetSelection()))
        secondFrame.Show()
########################################################################
class SKEditFrame(wx.Frame):
    '''
    Method that handles editing playlists frame
    '''
    
    def __init__(self, skm, editList):
        '''
        Gets passed the original and mediaManager
        '''
        self.editList = editList
        self.skm = skm
        wx.Frame.__init__(self,None,title='Playlist Management', size=(725,400))
        self.panel = wx.Panel(self)
        
        #Playlist choice display
        self.mediaDisplay = wx.ListBox(self.panel, size=(200,300),style=wx.LB_HSCROLL, choices = [])
        for x in self.skm.skdbGetAll():
            if(x=='_defPlaylist_OLD' or x==editList):
                pass
            elif(x=='defPlaylist'):
                self.mediaDisplay.Append('Library')
            else:
                self.mediaDisplay.Append(x)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.chooseList, self.mediaDisplay)


        #Create songs list display
        self.songDisplay = wx.ListBox(self.panel, size=(200,300),style=wx.LB_EXTENDED|wx.LB_HSCROLL, choices = [])
        for x in self.skm.skdbGetList('defPlaylist'):
            self.songDisplay.Append(x.title,x)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.addItem, self.songDisplay)
        
        self.editDisplay = wx.ListBox(self.panel, size=(200,300),style=wx.LB_EXTENDED|wx.LB_HSCROLL, choices = [])
        for x in self.skm.skdbGetList(editList):
            self.editDisplay.Append(x.title, x)        
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.remItem, self.editDisplay)

        
        self.addBtn = wx.Button(self.panel,label='>>|')
        self.addBtn.Bind(wx.EVT_BUTTON,self.addItems)
        self.remBtn = wx.Button(self.panel,label='|<<')
        self.remBtn.Bind(wx.EVT_BUTTON,self.remItems)

        font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
        lbl1 = wx.StaticText(self.panel,-1,style=wx.ALIGN_CENTER)
        lbl2 = wx.StaticText(self.panel,-1,style=wx.ALIGN_CENTER)
        lbl3 = wx.StaticText(self.panel,-1,style=wx.ALIGN_CENTER)
        lbl4 = wx.StaticText(self.panel,-1,style=wx.ALIGN_CENTER)

        lbl1.SetFont(font)
        lbl1.SetLabel('Playlist')
        lbl2.SetFont(font)
        lbl2.SetLabel('Songs')
        lbl3.SetFont(font)
        lbl3.SetLabel(editList + ': Songs')
        lbl4.SetLabel(' ')
        sizer = wx.GridBagSizer(0,0)
        sizer.Add(lbl1, pos=(0,0), flag=wx.ALL, border=5)
        sizer.Add(lbl2, pos=(0,1), flag=wx.ALL, border=5)
        sizer.Add(lbl3, pos=(0,3), flag=wx.ALL, border=5)
        sizer.Add(self.mediaDisplay, pos=(1,0), span=(9,0), flag=wx.EXPAND, border=5)
        sizer.Add(self.songDisplay, pos=(1,1), span=(9,1), flag=wx.EXPAND, border=5)
        sizer.Add(self.editDisplay, pos=(1,3), span=(9,1), flag=wx.EXPAND, border=5)
        sizer.Add(self.addBtn, pos=(4,2), flag=wx.ALL, border=5)
        sizer.Add(self.remBtn, pos=(5,2), flag=wx.ALL, border=5)

        self.panel.SetSizer(sizer)
        
    def chooseList(self, event):
        '''
        Method that populates song list from chosen playlist
        ''' 
        self.songDisplay.Clear()
        name = self.mediaDisplay.GetString(self.mediaDisplay.GetSelection())
        if(name=='Library'):
            name = 'defPlaylist'
        for x in self.skm.skdbGetList(name):
            self.songDisplay.Append(x.title,x)
            
    def addItems(self, event):
        '''
        Method that adds chosen songs to list
        '''
        toAdd = self.songDisplay.GetSelections()
        skFToAdd = []
        for x in toAdd:
            skFToAdd.append(self.songDisplay.GetClientData(x))
        if(len(toAdd)<1):
            #ERROR
            wx.MessageBox("DONT DO THAT","ERROR",wx.ICON_EXCLAMATION|wx.OK)
            return
        self.skm.skdbUpdateListMany(1,self.editList,skFToAdd)
#         for x in toAdd:
#             self.skm.skdbUpdateList(1,self.editList,self.songDisplay.GetClientData(x))
        self.editDisplay.Clear()
        for x in self.skm.skdbGetList(self.editList):
            self.editDisplay.Append(x.title, x)
            
    def addItem(self, event):
        '''
        Method that adds a singular song from double click
        '''
        toAdd = self.songDisplay.GetSelections()
        if(len(toAdd)<1):
            #ERROR
            wx.MessageBox("DONT DO THAT","ERROR",wx.ICON_EXCLAMATION|wx.OK)
            return
        for x in toAdd:
            self.skm.skdbUpdateList(1,self.editList,self.songDisplay.GetClientData(x))
        self.editDisplay.Clear()
        for x in self.skm.skdbGetList(self.editList):
            self.editDisplay.Append(x.title, x)
            
        
    def remItems(self, event):
        '''
        Method that removes chosen songs from edit list
        '''
        toRem = self.editDisplay.GetSelections()
        skFToRem = []
        for x in toRem:
            skFToRem.append(self.editDisplay.GetClientData(x))
        if(len(toRem)<1):
            #ERROR
            wx.MessageBox("DONT DO THAT","ERROR",wx.ICON_EXCLAMATION|wx.OK)
            return
        self.skm.skdbUpdateListMany(0,self.editList,skFToRem)
#         for x in toRem:
#             self.skm.skdbUpdateList(0,self.editList,self.editDisplay.GetClientData(x))
        self.editDisplay.Clear()
        for x in self.skm.skdbGetList(self.editList):
            self.editDisplay.Append(x.title, x)
        
    def remItem(self, event):
        '''
        Method that removes singular song from edit list
        '''
        toRem = self.editDisplay.GetSelections()
        if(len(toRem)<1):
            #ERROR
            wx.MessageBox("DONT DO THAT","ERROR",wx.ICON_EXCLAMATION|wx.OK)
            return
        for x in toRem:
            self.skm.skdbUpdateList(0,self.editList,self.editDisplay.GetClientData(x))
        self.editDisplay.Clear()
        for x in self.skm.skdbGetList(self.editList):
            self.editDisplay.Append(x.title, x)
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MediaFrame()
    frame.Show()
    app.MainLoop()
        
        
        