''' @author: Cody, Jamie '''

import wx
import wx.media
import os
from socket import gethostname, gethostbyname
import wx.lib.buttons as buttons
from SKHTTPClient import SKHTTPClient
from SKMedia import SKMedia
from SKFile import SKFile
import configparser
import http.client
import ipaddress
import time

# for future use
# import wx.lib.agw.aquabutton as AB

dirName = os.getcwd()
bitmapDir = os.path.join(dirName, 'bitmaps')


class SKGUI(wx.Panel):
    '''
    Class meant to build and operate the GUI. Due to MediaCTRL's operation
    the media player functions are wrapped in the GUI. This means that a
    command line only client isn't possible.
    '''

    def __init__(self, parent):
        '''
        Constructor

        mediaList keeps track of skFiles in the order they appear in the song display list.
        playIndex tracks the selection index of the list, so that
        next and previous commands can select 1 above or below that value from the mediaList.'
        '''
        wx.Panel.__init__(self, parent=parent)
        self.mediaManager = SKMedia()
        self.frame = parent
        self.currentVolume = 50
        self.createMenu()
        self.skc = self.skStartup()  # SKHTTPClient("C:\\SoundFiles\\Client\\", 1445, '127.0.0.1')
        val = self.createLayout()
        if val > 0:
            # Broken display
            return;

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self.frame.Bind(wx.EVT_CLOSE, self.skExitApp)
        self.timer.Start(100)
        self.mediaList = []
        self.playIndex = 0
        self.isPlaying = False
        self.uri = 'http://' + self.__host + ':' + str(self.__port) + '/'

    def skStartup(self):
        '''
        Method for either running setup wizard, or grabbing information from ini file.
        Returns a created SKHTTPClient to use for connections.
        '''

        dirName = os.path.dirname(os.path.realpath(__file__))
        if (os.path.isfile('sksettings.ini')):
            # Process ini file
            try:
                config = configparser.ConfigParser()
                config.read('sksettings.ini')
                self.__host = config['DEFAULT']['ServerIP']
                self.__port = int(config['DEFAULT']['ServerPort'])
                self.__customServer = int(config['DEFAULT']['CustomServer'])
                self.__dirLocation = config['DEFAULT']['ServerDirectoryFile']
                self.__timeout = float(config['DEFAULT']['ServerTimeout'])

                # self.__pass = config['DEFAULT']['ConnectionPassword']
                # self.__admPass = config['DEFAULT']['AdminPassword']
                return SKHTTPClient(self.__port, self.__host, self.__customServer, self.__timeout)
            except Exception as e:
                wx.MessageBox('Issue with INI file, please check settings', 'INI File', wx.ICON_EXCLAMATION)
                return SKHTTPClient(80, '127.0.0.1', 0, .5)

        else:
            result = wx.MessageBox("Welcome to SounderKin!\nPlease estabhlish a conneciton...", "Welcome",
                                   wx.ICON_QUESTION | wx.OK | wx.CANCEL)
            while result == wx.OK:
                while result == wx.OK:
                    '''Get IP'''
                    self.__host = self.skPopUpValue('Enter Server IP', '127.0.0.1')
                    try:
                        ipaddress.ip_address(self.__host)
                        if self.__host == '127.0.0.1' or self.__host == 'localhost':
                            try:
                                self.__host = gethostbyname(gethostname())
                            except Exception:
                                pass
                        else:
                            break
                    except:
                        wx.MessageBox("Enter a valid IP address", "IP Address", wx.ICON_EXCLAMATION | wx.OK)
                while True:
                    '''Get Port'''
                    try:
                        self.__port = int(self.skPopUpValue('Enter Server Port', '80'))
                        break
                    except:
                        wx.MessageBox("Enter a valid port", "Port Number", wx.ICON_EXCLAMATION | wx.OK)

                while True:
                    '''Get Timeout'''
                    try:
                        self.__timeout = float(self.skPopUpValue('Server Timeout (In Seconds)', '.5'))
                        break
                    except:
                        wx.MessageBox("Enter a valid time", "Timeout", wx.ICON_EXCLAMATION | wx.OK)

                '''Get Server Directory Location'''
                self.__dirLocation = self.skPopUpValue('Enter Location of Server directory file','directory.txt')

                '''Get if user is using SK server'''
                customServerVal = wx.MessageDialog(None,"Are you using the SKServer?", style=wx.YES_NO|wx.CENTRE).ShowModal()
                if(customServerVal==wx.ID_YES):
                    self.__customServer = 1
                else:
                    self.__customServer = 0
                # self.__pass = self.skPopUpValue('Connection Password', '')
                # self.__admPass = self.skPopUpValue('Enter Admin Password (if known)', '')
                try:
                    config = configparser.ConfigParser()
                    config['DEFAULT'] = {}
                    config['DEFAULT']['ServerIP'] = self.__host
                    config['DEFAULT']['ServerPort'] = str(self.__port)
                    config['DEFAULT']['CustomServer'] = str(self.__customServer)
                    config['DEFAULT']['ServerDirectoryFile'] = self.__dirLocation
                    config['DEFAULT']['ServerTimeout'] = str(self.__timeout)

                    # config['DEFAULT']['ConnectionPassword'] = self.__pass
                    # config['DEFAULT']['AdminPassword'] = self.__admPass
                    with open('sksettings.ini', 'w') as iniFile:
                        config.write(iniFile)
                except Exception as e:
                    wx.MessageBox('Issue with INI file, please set connection', 'INI File', wx.ICON_EXCLAMATION)
                return SKHTTPClient(self.__port, self.__host, self.__customServer, self.__timeout)
            if result == wx.CANCEL:
                self.skExitApp()

    def skUpdateIni(self):
        '''Method to update ini'''
        print("updating")
        try:
            config = configparser.ConfigParser()
            config['DEFAULT'] = {}
            config['DEFAULT']['ServerIP'] = self.__host
            config['DEFAULT']['ServerPort'] = str(self.__port)
            config['DEFAULT']['CustomServer'] = str(self.__customServer)
            config['DEFAULT']['ServerDirectoryFile'] = self.__dirLocation
            config['DEFAULT']['ServerTimeout'] = str(self.__timeout)
            # config['DEFAULT']['ConnectionPassword'] = self.__pass
            # config['DEFAULT']['AdminPassword'] = self.__admPass
            with open('sksettings.ini', 'w') as iniFile:
                config.write(iniFile)
        except Exception as e:
            wx.MessageBox('Issue with updating INI file', 'INI File', wx.ICON_EXCLAMATION)

    def skPopUpValue(self, text, defValue):
        '''
        Method that generates a pop up dialog box for errors
        '''
        popup = wx.TextEntryDialog(None, text, value=defValue)
        popup.ShowModal()
        value = popup.GetValue()
        popup.Destroy()
        return value

    def createLayout(self):
        '''
        Create layout of GUI

        The slider of the GUI needs an update as clicking on the bar doesn't move the slider to the
        correct position. This can cause weird stuff when you click multiple times. This isn't a simple fix,
        so I'd suggest starting here. This will be further complicated once we switch to streaming.

        https://stackoverflow.com/questions/9961456/get-wxpython-sliders-value-under-mouse-click
        '''
        try:
            self.mediaPlayer = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER, szBackend=wx.media.MEDIABACKEND_WMP10)
            self.Bind(wx.media.EVT_MEDIA_LOADED, self.loadPlay)
            self.mediaPlayer.Bind(wx.media.EVT_MEDIA_FINISHED, self.skNext, self.mediaPlayer)

        except Exception as e:
            # print(e)
            self.Destroy()
            self.skExitApp()
            return 1

        self.playSlider = wx.Slider(self, size=wx.DefaultSize, style=wx.SL_HORIZONTAL)
        self.Bind(wx.EVT_SLIDER, self.onSeek, self.playSlider)

        self.volumeCOP = wx.Slider(self, style=wx.SL_VERTICAL | wx.SL_INVERSE)
        self.volumeCOP.SetRange(0, 100)
        self.volumeCOP.SetValue(self.currentVolume)
        self.volumeCOP.Bind(wx.EVT_SLIDER, self.onSetVolume)

        self.mediaDisplay = wx.ListCtrl(self, size=(-1, 450), style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.mediaDisplay.InsertColumn(0, 'Song', width=150)
        self.mediaDisplay.InsertColumn(1, 'Artist', width=150)
        self.mediaDisplay.InsertColumn(2, 'Album', width=150)

        i = 0
        for x in self.skc.skGetFileDir():
            self.mediaList.append(x)
            self.mediaDisplay.Append([x.title, x.artist, x.album])
            self.mediaDisplay.SetItemData(i, int(x.index))
            i += 1

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.skGetFile, self.mediaDisplay)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.skSongRightClick, self.mediaDisplay)


        self.logo = wx.StaticBitmap(self,
                                    bitmap=wx.Bitmap((os.path.join(bitmapDir, "sounderkin.png")), wx.BITMAP_TYPE_ANY))

        self.hideButton = wx.Button(self, id=wx.ID_ANY, label='Hide List')
        self.hideButton.Bind(wx.EVT_BUTTON, self.onButton)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        audioSizer = self.buildAudioBar()
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)

        # layout widgets
        mainSizer.Add(self.playSlider, 1, wx.ALL | wx.EXPAND, 5)
        hSizer.Add(audioSizer, 0, wx.ALL | wx.CENTER, 5)
        hSizer.Add(self.volumeCOP, 0, wx.ALL, 5)
        bottomSizer.Add(self.logo, 0, wx.RIGHT, border=65)
        bottomSizer.Add(self.hideButton, 0, wx.TOP, border=7)
        mainSizer.Add(hSizer)
        leftSizer.Add(mainSizer, wx.ALIGN_TOP)
        leftSizer.Add(bottomSizer, wx.ALIGN_BOTTOM)
        topSizer.Add(leftSizer)
        topSizer.Add(self.mediaDisplay, 1, wx.RIGHT | wx.EXPAND, 5)

        self.SetSizer(topSizer)
        self.Layout()

        return 0

    def onButton(self, event):
        button = event.GetEventObject()
        if button.GetLabel() == 'Show List':
            button.SetLabel('Hide List')
            self.mediaDisplay.Show()
            self.frame.SetSize(800, 300)
        else:
            button.SetLabel('Show List')
            self.mediaDisplay.Hide()
            self.frame.SetSize(335, 300)

    def skSongRightClick(self, event):
        submenu = wx.Menu()
        self.keyVals = []
        for x in self.mediaManager.skdbGetAll():
            if (x == 'defPlaylist'):
                continue
            elif (x == '_defPlaylist_OLD'):
                continue
            # Append item to sub menubar
            newID = wx.Window.NewControlId()
            temp = submenu.AppendCheckItem(newID, x)
            #data = event.GetClientData()
            appendMe = (newID, x, event)
            self.keyVals.append(appendMe)
        rightMenu = wx.Menu()
        rightMenu.AppendSubMenu(submenu, "&Add to Playlist")
        # Bind function to it
        submenu.Bind(wx.EVT_MENU, self.menuhandler)
        self.mediaDisplay.PopupMenu( rightMenu, event.GetPoint() )
        rightMenu.Destroy() # destroy to avoid mem leak

    def menuhandler(self, event):
        id = event.GetId()
        for x in self.keyVals:
            if (x[0] == id):
                name = x[1]
                # data = self.mediaDisplay.GetItemData(x[2].GetIndex())
                playIndex = self.mediaDisplay.GetFocusedItem()
                # data = playIndex.GetClientData()
                value = self.skc.skCheckFile(playIndex)
                # print("val " + str(value))
                # data = data.GetClientData()
                # toAdd = self.sourceDisplay.GetSelections()
                # skFToAdd = []
                # for x in toAdd:
                #     skFToAdd.append(self.sourceDisplay.GetClientData(x))
                print("Right click file...\n\tPlaylist name: {0}\tData: {1}".format(name,playIndex))
                # self.mediaManager.skdbUpdateList(1, name, data)

    def buildAudioBar(self):
        """
        Builds the audio bar controls
        """
        audioBarSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.buildBtn({'bitmap': 'prev.png', 'handler': self.skPrev,
                       'name': 'prev'},
                      audioBarSizer)

        # create play/pause toggle button
        img = wx.Bitmap(os.path.join(bitmapDir, "play.png"))
        self.playPauseBtn = buttons.GenBitmapToggleButton(self, bitmap=img, name="play")
        # self.playPauseBtn = AB.AquaButton(self, bitmap=img)
        self.playPauseBtn.Enable(False)

        img = wx.Bitmap(os.path.join(bitmapDir, "pause.png"))
        self.playPauseBtn.SetBitmapSelected(img)
        self.playPauseBtn.SetInitialSize()

        self.playPauseBtn.Bind(wx.EVT_BUTTON, self.onPlay)
        audioBarSizer.Add(self.playPauseBtn, 0, wx.LEFT, 3)

        btnData = [{'bitmap': 'stop.png',
                    'handler': self.onStop, 'name': 'stop'},
                   {'bitmap': 'next.png',
                    'handler': self.skNext, 'name': 'next'}]
        for btn in btnData:
            self.buildBtn(btn, audioBarSizer)

        return audioBarSizer

    def buildBtn(self, btnDict, sizer):
        '''
        Check out wx.BitMap Button and combine with rest of build option
        '''
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
        conn_item = fileMenu.Append(wx.Window.NewControlId(), "&New Connection", "Connect to Server")
        settingsItem = fileMenu.Append(wx.Window.NewControlId(), "&Settings","Change Settings")
        exitItem = fileMenu.Append(wx.Window.NewControlId(), "&Quit\tCTRL+q", "Quit")
        menubar.Append(fileMenu, '&File')

        mediaMenu = wx.Menu()
        updateListItem = mediaMenu.Append(wx.Window.NewControlId(), "&Update Library\tCtrl+u", "Update Media Directory")
        listItem = mediaMenu.Append(wx.Window.NewControlId(), "&Playlists\tCTRL+p", "Create Playlist")
        shuffleItem = mediaMenu.Append(wx.Window.NewControlId(), '&Shuffle\tCTRL+s', 'Shuffle Current List')
        batchItem = mediaMenu.Append(wx.Window.NewControlId(), '&Batch Download\tCTRL+b', 'Batch Download')
        menubar.Append(mediaMenu, '&Media')

        controlMenu = wx.Menu()
        playItem = controlMenu.Append(wx.Window.NewControlId(), "&Play Song        Space", "Play Song")
        pauseItem = controlMenu.Append(wx.Window.NewControlId(), "&Pause Song     Space", "Pause Song")
        nextItem = controlMenu.Append(wx.Window.NewControlId(), "&Next Song               >", "Next Song")
        prevItem = controlMenu.Append(wx.Window.NewControlId(), "&Previous Song         <", "Previous Song")
        menubar.Append(controlMenu, '&Controls')

        self.frame.SetMenuBar(menubar)
        self.frame.Bind(wx.EVT_MENU, self.skSetConnection, conn_item)
        self.frame.Bind(wx.EVT_MENU, self.skEditSettings, settingsItem)
        self.frame.Bind(wx.EVT_MENU, self.skExitApp, exitItem)
        self.frame.Bind(wx.EVT_MENU, self.skGetList, updateListItem)
        self.frame.Bind(wx.EVT_MENU, self.skListOption, listItem)
        self.frame.Bind(wx.EVT_MENU, self.skShuffleList, shuffleItem)
        self.frame.Bind(wx.EVT_MENU, self.skBatchDownload, batchItem)
        self.frame.Bind(wx.EVT_MENU, self.onPlay, playItem)
        self.frame.Bind(wx.EVT_MENU, self.onPause, pauseItem)
        self.frame.Bind(wx.EVT_MENU, self.skNext, nextItem)
        self.frame.Bind(wx.EVT_MENU, self.skPrev, prevItem)

    def skExitApp(self, event):
        '''Method runs when user hits close'''
        self.frame.Destroy()
        self.skUpdateIni()

    def skEditSettings(self, event):
        # Change settings within SKSettings file
        print("timeout before: {0}".format(self.__timeout))
        dlg = EditConnection(self.frame)
        value = dlg.ShowModal()
        print("timout after: {0}".format(self.__timeout))
        if (value == 1):
            self.skUpdateIni()

    def skSetConnection(self, event):
        '''
        When user clicks connect from menu, a window that allows a user to change settings at once appears.
        On okay, would try a connection with the new options.
        '''
        dlg = NewConnection(parent=self)
        dlg.ShowModal()
        if dlg.resultip:
            try:
                ipaddress.ip_address(dlg.resultip)
            except:
                wx.MessageBox("Invalid IP", "ERROR", wx.ICON_EXCLAMATION | wx.OK)
                return
            self.__host = dlg.resultip
            self.__port = int(dlg.resultport)
        else:
            dlg.Destroy()
            return
        dlg.Destroy()

        self.skc = SKHTTPClient(self.__port, self.__host, self.__customServer, self.__timeout);
        self.connected = self.skc.skTestConnection()
        if (self.connected == 1):
            wx.MessageBox("Unable to connect to server, check settings", "ERROR", wx.ICON_EXCLAMATION | wx.OK)
            return
        wx.MessageBox("Server Connection Verified", "SUCCESS", wx.ICON_EXCLAMATION | wx.OK)

    def skBatchDownload(self, event):
        batchFrame = SKBatchFrame(self.mediaManager)
        batchFrame.ShowModal()
        if batchFrame.selection:
            if (batchFrame.selType == 'Playlists'):
                dList = self.mediaManager.skdbGetList(batchFrame.selection)
            elif (batchFrame.selType == 'Artists'):
                dList = self.mediaManager.skdbSearchList(2, batchFrame.selection, 'defPlaylist')
            elif (batchFrame.selType == 'Albums'):
                dList = self.mediaManager.skdbSearchList(3, batchFrame.selection, 'defPlaylist')
            # batchDlFrame = SKBatchDlFrame(dList, self.skc)
            # batchDlFrame.ShowModal()
            batchDLFrame = wx.GenericProgressDialog('','Downloading Files', maximum=len(dList), style=wx.PD_CAN_ABORT)
            batchDLFrame.Show()
            val = 0
            for x in dList:
                self.skc.skBatchFile(int(x.index), batchFrame.selection)
                val += 1
                check = batchDLFrame.Update(val)
                if not check:
                    break
        else:
            return

    def skGetList(self, event):
        '''
        Method for updating default display list
        '''
        check = self.skc.skBuildDir(self.__dirLocation)
        if (check == 2):
            wx.MessageBox("Unable to connect to server, check settings", "ERROR", wx.ICON_EXCLAMATION | wx.OK)
            return
        if(check == 1):
            wx.MessageBox("Something wen't wrong with directory building", "ERROR", wx.ICON_EXCLAMATION | wx.OK)
            return
        self.onStop(wx.EVT_BUTTON)
        self.playIndex = 0
        self.mediaList = []
        self.mediaDisplay.DeleteAllItems()
        i = 0
        for x in self.skc.skGetFileDir():
            self.mediaList.append(x)
            self.mediaDisplay.Append([x.title, x.artist, x.album])
            self.mediaDisplay.SetItemData(i, int(x.index))
            i += 1
        self.mediaManager.skdbUpdateDefault(self.mediaList)

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
        # ----------------------REPORT VERSION----------------------#
        self.mediaList = []
        self.mediaDisplay.DeleteAllItems()
        if (name == 'Library'):
            name = 'defPlaylist'
        i = 0
        vals = self.mediaManager.skdbGetList(name)
        for x in vals:
            self.mediaList.append(x)
            self.mediaDisplay.Append([x.title, x.artist, x.album])
            self.mediaDisplay.SetItemData(i, int(x.index))
            i += 1
        self.playIndex = 0
        event.Skip()

    def skSortList(self, event):
        '''
        Method that handles list sort based on header clicked
        Please implement once display method is chosen.
        '''

    def skShuffleList(self, event):
        '''
        Method that shuffles currently selected list
        '''
        # ----------------------REPORT VERSION----------------------#
        findDex = self.mediaList[self.playIndex]
        tempList = self.mediaManager.skShuffleList(self.mediaList, self.playIndex)
        self.mediaList = []
        self.mediaDisplay.DeleteAllItems()
        i = 0
        for x in tempList:
            self.mediaDisplay.Append([x.title, x.artist, x.album])
            self.mediaDisplay.SetItemData(i, int(x.index))
            self.mediaList.append(x)
            i += 1
        self.playIndex = 0

    def skGetFile(self, event):
        '''
        Method for downloading a music file, upon finishing download, play music
        '''
        indexSKF = self.mediaDisplay.GetItemData(event.GetIndex())
        self.playIndex = self.mediaDisplay.GetFocusedItem()  # self.mediaDisplay.GetSelection()
        # Song's unique index
        self.playIndex = self.mediaDisplay.GetFocusedItem()
        index = int(indexSKF)
        try:
            # Has a song been played yet, avoid attempted load of current song
            self.currentSong
        except AttributeError:
            cs = False
        else:
            cs = True
        if (cs):
            # Start current song over again
            if (self.currentSong == index):  # skf.index):
                self.skLoadMusic(self.skc.skGetFileDir()[index].path, index)
                return
        # if val == 0:
            # continue
        # In future use HEAD to confirm file exists before loading (Done in loadMusic method
        self.skLoadMusic(self.skc.skGetFileDir()[index].path, index)
        self.currentSong = index
        # else:
            # wx.MessageBox("Unable to load %s: No file found" % self.mediaList[index].title, "ERROR",
            #               wx.ICON_EXCLAMATION | wx.OK)

    def skLoadMusic(self, musicPath, index):
        """
        Load the music into the MediaCtrl or display an error dialog
        if the user tries to load an unsupported file type
        """
        val = self.skc.skCheckFile(index)
        print("val: " + str(val))
        if(val==1):
            wx.MessageBox("Unable to load %s: No file found" % self.mediaList[index].title, "ERROR",wx.ICON_EXCLAMATION | wx.OK)
            return
        elif(val==2):
            wx.MessageBox("Unable to connect to server, check settings", "ERROR", wx.ICON_EXCLAMATION | wx.OK)
            return
        request = self.uri + musicPath
        print("Request: " + request)
        if not self.mediaPlayer.Load(musicPath):
            wx.MessageBox("Unable to load %s: Unsupported format?" % musicPath,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mediaPlayer.SetInitialSize()
            self.GetSizer().Layout()
            self.playSlider.SetRange(0, self.mediaList[self.playIndex].time * 1000)
            # self.playSlider.SetRange(0, self.mediaPlayer.Length())
            self.playPauseBtn.Enable(True)

    def skNext(self, event):
        """
        Method that selects next song from list, or stops if end of list is reached.
        """
        # ----------------------REPORT VERSION----------------------#
        if (len(self.mediaList) < 1):
            return
        self.mediaPlayer.Stop()
        # Stop if final song
        if (self.playIndex == len(self.mediaList) - 1):
            self.onStop(wx.EVT_CATEGORY_ALL)
            return
        # Get song after current song, playIndex tracks index in the playlist, in case the selection is moved,
        # But a new song is not chosen.

        index = self.mediaDisplay.GetItemData(self.playIndex + 1)
        # Potential use of HEAD request to confirm file's existence before loading
        self.skLoadMusic(self.skc.skGetFileDir()[index].path, index)
        self.mediaDisplay.Select(self.playIndex + 1, True)
        self.mediaDisplay.SetItemState(self.playIndex + 1, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        self.currentSong = index
        self.playIndex += 1
        # else:
        #     wx.MessageBox("Unable to load %s: No file found" % self.mediaList[index].title, "ERROR",
        #                   wx.ICON_EXCLAMATION | wx.OK)

    def skPrev(self, event):
        """
        Method that loads up the previous song, based on playlist order.

        Here is where you could try media ctrl's length() command
        """
        # ----------------------REPORT VERSION----------------------#
        self.mediaPlayer.Stop()
        if (self.playIndex == 0):
            self.onStop(wx.EVT_CATEGORY_ALL)
            return
        index = self.mediaDisplay.GetItemData(self.playIndex - 1)
        self.skLoadMusic(self.skc.skGetFileDir()[index].path, index)
        self.mediaDisplay.Select(self.playIndex - 1, True)
        self.currentSong = index
        self.playIndex -= 1
        # else:
        #     wx.MessageBox("Unable to load %s: No file found" % self.mediaList[index], "ERROR",
        #                   wx.ICON_EXCLAMATION | wx.OK)

    def onPause(self):
        self.mediaPlayer.Pause()
        self.isPlaying = False

    def onPlay(self, event):
        """
        Plays the music
        """
        # Jamie: look into this for checking if playing
        if self.isPlaying:
            self.onPause()
            return

        if not self.mediaPlayer.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.isPlaying = True
            self.mediaPlayer.SetInitialSize()
            self.GetSizer().Layout()
            self.playSlider.SetRange(0, self.mediaList[self.playIndex].time * 1000)
            # self.playSlider.SetRange(0, self.mediaPlayer.Length())

        event.Skip()

    def loadPlay(self, event):
        '''
        Method that plays the loaded music automatically
        '''
        self.mediaPlayer.Play()
        # self.mediaPlayer.SetInitialSize()
        # self.GetSizer().Layout()
        # self.playSlider.SetRange(0, self.mediaList[self.playIndex].time*1000)
        # self.playSlider.SetRange(0, self.mediaPlayer.Length())
        self.playPauseBtn.SetValue(True)

    def skCheckMedia(self, event):
        index = self.mediaDisplay.GetItemData(self.playIndex)
        songMax = self.mediaList[index].time
        currentTime = self.mediaPlayer.Length()
        print('songMax ' + str(songMax))
        print('currentTime: ' + str(currentTime))
        if (float(songMax) > float(currentTime)):
            event.Veto()

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
        self.mediaPlayer.SetVolume(float(self.currentVolume / 100))

    def onStop(self, event):
        """
        Stops the music and resets the play button
        """
        self.mediaPlayer.Stop()
        self.isPlaying = False
        self.playPauseBtn.SetToggle(False)

    def onTimer(self, event):
        """
        Keeps the player slider updated
        """
        try:
            offset = self.mediaPlayer.Tell()
            self.playSlider.SetValue(offset)
        except RuntimeError:
            pass #Closed app while trying to get time for slider, unimportant


########################################################################
class MediaFrame(wx.Frame):
    def __init__(self):
        setSize = (800, 300)
        wx.Frame.__init__(self, None, wx.ID_ANY, "SounderKin 0.2", size=setSize)
        self.panel = SKGUI(self)

        self.panel.Bind(wx.EVT_KEY_DOWN, self.onChar)

        self.logo = wx.Icon(wx.Bitmap((os.path.join(bitmapDir, "logo.ico")), wx.BITMAP_TYPE_ANY))
        self.SetIcon(self.logo)

    def onChar(self,event):
        keycode = event.GetKeyCode()
        if (keycode == wx.WXK_LEFT):
            self.panel.skPrev(self)
            return
        elif (keycode == wx.WXK_RIGHT):
            self.panel.skNext(self)
            return
        elif (keycode == wx.WXK_SPACE):
            if (self.panel.isPlaying == False):
                self.panel.onPlay(self)
            else:
                self.panel.onPause(self)
            return

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
        wx.Frame.__init__(self, None, title='Playlist Management', size=(300, 300))
        self.panel = wx.Panel(self)
        # Create List Display
        self.mediaDisplay = wx.ListBox(self.panel, size=(275, 150), style=wx.LB_HSCROLL, choices=[])
        # Jamie:
        # The only time this doesn't work is if you click to edit a playlist
        # Then try to load the playlist from within the edit page
        # however there's not a playlist sellected so it seg faults - TBD
        self.mediaDisplay.Bind(wx.EVT_LISTBOX_DCLICK,
                               lambda event: parent.skLoadList(event, self.mediaDisplay.GetString(
                                   self.mediaDisplay.GetSelection())),
                               self.mediaDisplay)
        self.mediaDisplay.Bind(wx.EVT_LISTBOX_DCLICK, self.chooseList, self.mediaDisplay)
        self.refresh()
        self.newBtn = wx.Button(self.panel, label='Create')
        self.newBtn.Bind(wx.EVT_BUTTON, self.newList)
        self.editBtn = wx.Button(self.panel, label='Edit')
        self.editBtn.Bind(wx.EVT_BUTTON, self.editList)
        self.dlBtn = wx.Button(self.panel, label='Delete')
        self.dlBtn.Bind(wx.EVT_BUTTON, self.delList)

        font = wx.Font(16, wx.ROMAN, wx.ITALIC, wx.NORMAL)
        lbl1 = wx.StaticText(self.panel, -1, style=wx.ALIGN_CENTER)
        lbl1.SetFont(font)
        lbl1.SetLabel('Playlists')

        self.frameSizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.newBtn, 0, wx.ALL | wx.EXPAND, 5)
        btnSizer.Add(self.dlBtn, 0, wx.ALL | wx.EXPAND, 5)
        btnSizer.Add(self.editBtn, 0, wx.ALL | wx.EXPAND, 5)

        sizer.Add(lbl1, 0, wx.ALL, 5)
        sizer.Add(self.mediaDisplay, 0, wx.ALL, 5)
        sizer.Add(btnSizer, 0)

        #-----------------------------------------------------------------------
        # BEGIN CREATING PLAYLIST EDIT SIDE PANEL
        sourceSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        songSizer = wx.BoxSizer(wx.VERTICAL)

        #-----------------------------------------------------------------------
        # LIST THAT DISPLAY WHERE THE SONGS ARE CHOSEN FROM
        sourceLabel = wx.StaticText(self.panel, -1, style=wx.ALIGN_CENTER)
        sourceLabel.SetLabel('Choose a Source:')

        choiceList = ['Source','Albums','Artists','Library']
        self.choiceBox = wx.Choice(self.panel,choices=choiceList)
        self.choiceBox.Bind(wx.EVT_CHOICE,self.sourceChoice)

        self.sourceDisplay = wx.ListBox(self.panel, size=(175, 300), style=wx.LB_HSCROLL | wx.LB_SINGLE, choices=[])
        self.sourceDisplay.Clear()
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.sourceDoubleClick, self.sourceDisplay)

        sourceSizer.Add(sourceLabel, 0, wx.LEFT, border=10)
        sourceSizer.Add(self.choiceBox, 0, wx.ALL, border=10)
        sourceSizer.Add(self.sourceDisplay, 0, wx.ALL, border=10)

        #-----------------------------------------------------------------------
        # ADD AND REMOVE SONG BUTTONS FROM PLAYLIST PANEL
        self.addBtn = wx.Button(self.panel, label='Add >')
        self.addBtn.Bind(wx.EVT_BUTTON, self.addItems)
        self.remBtn = wx.Button(self.panel, label='< Remove')
        self.remBtn.Bind(wx.EVT_BUTTON, self.remItems)
        buttonSizer.Add(self.addBtn, 0, wx.ALIGN_CENTER | wx.TOP, border=150)
        buttonSizer.Add(self.remBtn, 0, wx.ALIGN_CENTER | wx.ALL, border=10)

        #-----------------------------------------------------------------------
        # LAST LIST THAT SHOWS THE PLAYLISTS CONTENTS
        self.songDisplay = wx.ListBox(self.panel, size=(175,350), style=wx.LB_EXTENDED | wx.LB_HSCROLL, choices=[])
        songSizer.Add(self.songDisplay, 0, wx.ALL, border=10)

        #-----------------------------------------------------------------------
        # ADDING BOTH BOX SIZERS TO THE TOP BOX SIZER
        listsSizer = wx.BoxSizer(wx.HORIZONTAL)
        listsSizer.Add(sourceSizer)
        listsSizer.Add(buttonSizer, wx.ALIGN_CENTER)
        listsSizer.Add(songSizer)

        #-----------------------------------------------------------------------
        # BOTTOM BOX SIZER - JUST BUTTONS THAT USER CAN CLICK
        self.saveBtn = wx.Button(self.panel, label="Save && Load Playlist")
        self.saveBtn.Bind(wx.EVT_BUTTON, self.saveOpr)
        self.saveBtn.Bind(wx.EVT_BUTTON,
                               lambda event: parent.skLoadList(event, self.mediaDisplay.GetString(
                                   self.mediaDisplay.GetSelection())))
        self.cancelBtn = wx.Button(self.panel, label='Cancel')
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.cancelOpr)
        saveSizer = wx.BoxSizer(wx.HORIZONTAL)
        saveSizer.Add(self.cancelBtn, flag=wx.LEFT, border=250)
        saveSizer.Add(self.saveBtn, flag=wx.LEFT, border=15)

        #-----------------------------------------------------------------------
        # ADDING BOTH TOP AND BOTTOM BOX SIZERS TO MAIN SIZER
        self.overallSizer = wx.BoxSizer(wx.VERTICAL)
        self.overallSizer.Add(listsSizer, flag=wx.ALIGN_TOP, border=1)
        self.overallSizer.Add(saveSizer, flag=wx.ALIGN_BOTTOM, border=1)

        self.frameSizer.Add(sizer, 0)
        self.frameSizer.Add(self.overallSizer, 0)
        self.frameSizer.Show(self.overallSizer, show=False)

        self.panel.SetSizer(self.frameSizer)
        self.panel.Layout()

    #---------------------------------------------------------------------------
    # THIS WILL DETEMINE WHICH SOURCE TYPE WAS PICKED AND DISPLAY IT WITHIN BOX
    def sourceChoice(self, event):
        option = self.choiceBox.GetString(self.choiceBox.GetSelection())
        if(option == '' or option == ''):
            return
        self.sourceDisplay.Clear()
        if(option == 'Albums'):
            '''db access albums'''
            dispList = self.skm.skdbGetUniques('album')
            for x in dispList:
                self.sourceDisplay.Append(x)
        elif(option == 'Artists'):
            '''db display artist'''
            dispList = self.skm.skdbGetUniques('artist')
            for x in dispList:
                self.sourceDisplay.Append(x)
        elif(option == 'Library'):
            '''db access entire library'''
            for x in self.skm.skdbGetList('defPlaylist'):
                self.sourceDisplay.Append(x.title, x)

    def newList(self, event):
        dlg = wx.TextEntryDialog(self, 'Enter List Name', 'Name Playlist')
        dlg.SetValue('Enter a name...')
        if dlg.ShowModal() == wx.ID_OK:
            val = self.skm.skdbNewList(dlg.GetValue())
            if val == 1:
                ''' Error Report '''
                wx.MessageBox("Issue creating list", "ERROR", wx.ICON_EXCLAMATION | wx.OK)
        dlg.Destroy()
        self.refresh()

    def delList(self, event):
        plIndex = self.mediaDisplay.GetSelection()
        if (plIndex != wx.NOT_FOUND):
            plName = self.mediaDisplay.GetString(plIndex)
            if (plName == 'Library'):
                wx.MessageBox("DONT DO THAT", "ERROR", wx.ICON_EXCLAMATION | wx.OK)
                return
            self.skm.skdbRemoveList(plName)
            self.refresh()
        else:
            wx.MessageBox("Please make sure a playlist is selected.", "Error", wx.OK)
            return

    def refresh(self):
        self.mediaDisplay.Clear()
        for x in self.skm.skdbGetAll():
            if (x == '_defPlaylist_OLD'):
                pass
            elif (x == 'defPlaylist'):
                self.mediaDisplay.Append('Library')
            else:
                self.mediaDisplay.Append(x)

    def refreshSongs(self, playlistName):
        self.songDisplay.Clear()
        for x in self.skm.skdbGetList(playlistName):
            self.songDisplay.Append(x.title, x)

    def editList(self, event):
        index = self.mediaDisplay.GetSelection()
        if (index != wx.NOT_FOUND):
            if (self.mediaDisplay.GetString(index) == 'Library'):
                wx.MessageBox("DONT DO THAT", "ERROR", wx.ICON_EXCLAMATION | wx.OK)
                return
            else:
                self.SetSize(wx.Size(800,450))
                self.frameSizer.Show(self.overallSizer, show=True)
                self.panel.SetSizer(self.frameSizer)
                self.panel.Layout()
                self.songDisplay.Clear()
                self.editList = self.mediaDisplay.GetString(self.mediaDisplay.GetSelection())
                name = self.editList
                # print("Selection: {0}\n".format(name))
                if (name == 'Library'):
                    name = 'defPlaylist'
                for x in self.skm.skdbGetList(name):
                    self.songDisplay.Append(x.title, x)
        else:
            wx.MessageBox("Please pick a playlist.", "Error", wx.OK)
            return

    def chooseList(self, event):
        '''
        Method that populates song list from chosen playlist
        '''
        self.songDisplay.Clear()
        index = self.mediaDisplay.GetSelection()
        if (index != wx.NOT_FOUND):
            name = self.mediaDisplay.GetString(index)
            if (name == 'Library'):
                name = 'defPlaylist'
            for x in self.skm.skdbGetList(name):
                self.songDisplay.Append(x.title, x)
            self.Destroy()
            event.Skip()
        else:
            wx.MessageBox("Error loading song", "error", wx.OK)
            return

    #---------------------------------------------------------------------------
    # WHEN SOMETHING IS DOUBLE CLICKED WITHIN THE SOURCE WINDOW IT WILL EITHER
    # OPEN THAT FOLDER OR ADD THAT SONG TO THE PLAYLIST
    def sourceDoubleClick(self, event):
        chosenIndex = self.sourceDisplay.GetSelection()
        if(chosenIndex != wx.NOT_FOUND):
            chosen = self.sourceDisplay.GetString(chosenIndex)
            inLibrary = False

            for x in self.skm.skdbGetList('defPlaylist'):
                if (x.title == chosen):
                    inLibrary = True

            if (inLibrary):
                toAdd = self.sourceDisplay.GetSelections()

                if (len(toAdd) < 1):
                    return

                for x in toAdd:
                    self.skm.skdbUpdateList(1, self.editList, self.sourceDisplay.GetClientData(x))

                self.songDisplay.Clear()

                for x in self.skm.skdbGetList(self.editList):
                    self.songDisplay.Append(x.title, x)

            else:
                choiceIndex = self.choiceBox.GetSelection()

                if (choiceIndex != wx.NOT_FOUND):

                    sourceIndex = self.sourceDisplay.GetSelection()

                    if (sourceIndex != wx.NOT_FOUND):

                        source = self.sourceDisplay.GetString(sourceIndex)

                        option = self.choiceBox.GetString(choiceIndex)
                        if(option == ''):
                            return

                        self.sourceDisplay.Clear()
                        results = []
                        libraryList = self.skm.skdbGetList('defPlaylist')

                        if(option == 'Albums'):
                            for x in libraryList:
                                if (source == x.album):
                                    print("album, {0}, {1}\n".format(source, x.album))
                                    results.append(x)

                        elif(option == 'Artists'):
                            for x in libraryList:
                                if (source == x.artist):
                                    print("artist, {0}, {1}\n".format(source, x.artist))
                                    results.append(x)

                        for x in results:
                            self.sourceDisplay.Append(x.title, x)
                    else:
                        wx.MessageBox("Could not read double click", "error", wx.OK)
                        return
                else:
                    wx.MessageBox("Please check to make sure you have a source selected", "info", wx.OK)
                    return
        else:
            wx.MessageBox("Please make sure a playlist is selected.", "Error", wx.OK)
            return

    #---------------------------------------------------------------------------
    # WHEN A SONG IS SELECTED AND THE ADD BUTTON IS PRESSED, THE SONG WILL BE
    # ADDED TO THE PLAYLIST IF IT IS NOT AN ACTUAL SONG, A MESSAGEBOX WILL SHOW
    def addItems(self, event):
        chosenIndex = self.sourceDisplay.GetSelection()
        if(chosenIndex != wx.NOT_FOUND):
            chosen = self.sourceDisplay.GetString(chosenIndex)

            inLibrary = False
            for x in self.skm.skdbGetList('defPlaylist'):
                if (x.title == chosen):
                    inLibrary = True

            if (inLibrary):

                toAdd = self.sourceDisplay.GetSelections()
                skFToAdd = []
                for x in toAdd:
                    skFToAdd.append(self.sourceDisplay.GetClientData(x))
                if (len(toAdd) < 1):
                    # ERROR
                    # wx.MessageBox("DONT DO THAT","ERROR",wx.ICON_EXCLAMATION|wx.OK)
                    return

                self.skm.skdbUpdateListMany(1, self.editList, skFToAdd)

                self.songDisplay.Clear()

                for x in self.skm.skdbGetList(self.editList):
                    self.songDisplay.Append(x.title, x)

            else:
                wx.MessageBox("Please select a song, not a source", "Error", wx.OK)
                return
        else:
            wx.MessageBox("Please make sure a playlist is selected.", "Error", wx.OK)
            return

    def remItems(self, event):
        '''
        Method that removes chosen songs from edit list
        '''
        toRem = self.songDisplay.GetSelections()
        skFToRem = []
        for x in toRem:
            skFToRem.append(self.songDisplay.GetClientData(x))
        if (len(toRem) < 1):
            # ERROR
            # wx.MessageBox("DONT DO THAT","ERROR",wx.ICON_EXCLAMATION|wx.OK)
            return
        self.skm.skdbUpdateListMany(0, self.editList, skFToRem)
        self.songDisplay.Clear()
        for x in self.skm.skdbGetList(self.editList):
            self.songDisplay.Append(x.title, x)

    def remItem(self, event):
        '''
        Method that removes singular song from edit list
        '''
        toRem = self.songDisplay.GetSelections()
        if (len(toRem) < 1):
            # ERROR
            # wx.MessageBox("DONT DO THAT","ERROR",wx.ICON_EXCLAMATION|wx.OK)
            return
        for x in toRem:
            self.skm.skdbUpdateList(0, self.editList, self.songDisplay.GetClientData(x))
        self.songDisplay.Clear()
        for x in self.skm.skdbGetList(self.editList):
            self.songDisplay.Append(x.title, x)

    def saveOpr(self, event):
        chosenIndex = self.mediaDisplay.GetSelection()
        if(chosenIndex != wx.NOT_FOUND):
            self.Destroy()
            event.Skip()
        else:
            wx.MessageBox("Please make sure you select a playlist to load", "Error", wx.OK)

    def cancelOpr(self, event):
        '''Method runs when user hits close'''
        self.Destroy()


#####################################################################################
class NewConnection(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Name Input", size=(650, 220))
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.iplabel = wx.StaticText(self.panel, label="IP Address", pos=(20, 20))
        self.ip = wx.TextCtrl(self.panel, value="", pos=(110, 20), size=(500, -1))
        self.portlabel = wx.StaticText(self.panel, label="Port Number", pos=(20, 60))
        self.port = wx.TextCtrl(self.panel, value="", pos=(110, 60), size=(500, -1))
        self.saveButton = wx.Button(self.panel, label="OK", pos=(110, 160))
        self.closeButton = wx.Button(self.panel, label="Cancel", pos=(210, 160))
        self.saveButton.Bind(wx.EVT_BUTTON, self.skSaveConn)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        # self.Show()

    def OnQuit(self, event):
        self.resultip = None
        self.Destroy()

    def skSaveConn(self, event):
        self.resultip = self.ip.GetValue()
        if self.resultip == '127.0.0.1' or self.resultip == 'localhost':
            try:
                self.resultip = gethostbyname(gethostname())
            except Exception:
                pass
        self.resultport = self.port.GetValue()
        self.Destroy()

#####################################################################################

class EditConnection(wx.Dialog):
    def __init__(self, parent):
        self.parent = parent
        self.frame = wx.Dialog.__init__(self, parent, wx.ID_ANY, "Edit Connection Settings", size=(650, 300))
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.iplabel = wx.StaticText(self.panel, label="IP Address", pos=(20, 20))
        self.ip = wx.TextCtrl(self.panel, value="", pos=(150, 20), size=(400, -1))
        self.portlabel = wx.StaticText(self.panel, label="Port Number", pos=(20, 60))
        self.port = wx.TextCtrl(self.panel, value="", pos=(150, 60), size=(400, -1))
        self.serverLabel = wx.StaticText(self.panel, label="Server Directory", pos=(20, 100))
        self.server = wx.TextCtrl(self.panel, value="", pos=(150, 100), size=(400, -1))
        self.timeoutLabel = wx.StaticText(self.panel, label="Server Timeout", pos=(20, 140))
        self.timeout = wx.TextCtrl(self.panel, value="", pos=(150, 140), size=(400, -1))
        self.custServerLabel = wx.StaticText(self.panel, label="Running the server? y or n", pos=(20, 180))
        self.custServer = wx.TextCtrl(self.panel, value="", pos=(150, 180), size=(400, -1))

        self.saveButton = wx.Button(self.panel, label="OK", pos=(110, 240))
        self.closeButton = wx.Button(self.panel, label="Cancel", pos=(210, 240))

        self.saveButton.Bind(wx.EVT_BUTTON, self.skSaveConn)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

    def OnQuit(self, event):
        self.resultip = None
        # self.frame.MakeModal(False)
        # self.Destroy()
        self.EndModal(0)

    def skSaveConn(self, event):
        if (self.ip.GetValue() != ""):
            self.parent.__host = self.ip.GetValue()

        if (self.port.GetValue() != ""):
            self.parent.__port = self.port.GetValue()

        if (self.custServer.GetValue() != ""):
            self.parent.__customServer = self.custServer.GetValue()

        if (self.server.GetValue() != ""):
            self.parent.__dirLocation = self.server.GetValue()

        if (self.timeout.GetValue() != ""):
            self.parent.__timeout = self.timeout.GetValue()

        self.EndModal(1)

#####################################################################################
class SKBatchFrame(wx.Dialog):
    '''
    Method that handles editing batch download frame
    '''

    def __init__(self, skm):
        '''
        Gets passed the original and mediaManager
        '''

        self.skm = skm
        wx.Dialog.__init__(self, None, title='Batch Management', size=(250, 450))
        self.panel = wx.Panel(self)
        choiceList = ['Albums','Artists','Playlists']
        self.choiceBox = wx.Choice(self.panel,choices=choiceList, size=(150,25))
        self.choiceBox.Bind(wx.EVT_CHOICE,self.skOnChoice)
        self.batchDisplay = wx.ListBox(self.panel, size=(200, 300), style=wx.LB_SINGLE | wx.LB_HSCROLL, choices=[])
        self.batchButton = wx.Button(self.panel, label="Batch Download", pos=(110, 160))
        self.batchButton.Bind(wx.EVT_BUTTON, self.skOnBatch)
        mainSizer = wx.GridBagSizer(0,0)
        mainSizer.Add(self.choiceBox, pos=(0,0), flag=wx.ALL, border=5)
        mainSizer.Add(self.batchDisplay, pos=(1,0), flag=wx.ALL, border=5)
        mainSizer.Add(self.batchButton, pos=(2,0), flag=wx.ALL, border=5)
        self.panel.SetSizer(mainSizer)
        self.selection = None
        self.selType = None

    def skOnChoice(self, event):
        option = self.choiceBox.GetString(self.choiceBox.GetSelection())
        if(option == '' ):
            return
        self.batchDisplay.Clear()
        if(option == 'Albums'):
            '''db access albums'''
            dispList = self.skm.skdbGetUniques('album')
            for x in dispList:
                self.batchDisplay.Append(x)
        elif(option == 'Artists'):
            '''db display artist'''
            dispList = self.skm.skdbGetUniques('artist')
            for x in dispList:
                self.batchDisplay.Append(x)
        elif(option == 'Playlists'):
            '''db access playlists'''
            for x in self.skm.skdbGetAll():
                if (x == '_defPlaylist_OLD'):
                    pass
                elif (x == 'defPlaylist'):
                    pass
                else:
                    self.batchDisplay.Append(x)

    def skOnBatch(self, event):
        '''User hit batch button'''
        try:
            self.selType = self.choiceBox.GetString(self.choiceBox.GetSelection())
            self.selection = self.batchDisplay.GetString(self.batchDisplay.GetSelection())
            self.Destroy()
        except:
            pass



# ----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MediaFrame()
    frame.Show()
    app.MainLoop()
