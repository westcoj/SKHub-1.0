'''
Created on Sep 21, 2018

@author: Cody
'''

import os
import random
from SKFile import SKFile
import sqlite3
import re

class SKMedia(object):
    '''
    This class is used to handle play list operations for the client. Using database tables, it
    keeps track of the default list and every list. 
    
    This needs more cleaning up, since text file tracking is no longer in use.
    '''


    def __init__(self):
        '''
        Constructor to set up media handler
        '''
        self.__regex = '[^0-9a-zA-Z ]+'
        self.__list = [] 
        self.__cacheList = []
        self.__listIndex = 0
        self.__dirName = os.getcwd()
        self.__plPath = os.path.join(self.__dirName, 'playlists')
        self.__dbPath = os.path.join(self.__dirName, 'playlists\\db.sqlite3')
        if not os.path.isdir(self.__plPath):
            os.makedirs(self.__plPath)
        #os.chdir(plPath)
        #self.skLoadList('default.pl')
        
         
    def skShuffleList(self,listcon, saveDex):
        '''
        Method for shuffling a list, shuffles the list in place so a copy
        must be used. Keeps note of current index to place at top of shufflie list
        '''
        listCopy = listcon
        saveFile = listCopy.pop(saveDex)
        random.shuffle(listCopy)
        listCopy.insert(0,saveFile)
        return listCopy
            
    #----------------------------------------DB METHODS-------------------------#
    
    def skScrubName(self, name):
        '''
        This method is meant to scrub play list name inputs to prevent SQLI and allow for spaces.
        '''
        return re.sub(self.__regex,'',name)
        
    
    def skdbGetList(self, name):
        '''
        Method for obtaining a table from the database and returning its contents
        
        UPDATE: Change name to be a variable, do not allow for SQL Injection
        '''
        retList = []
        try:
            con = sqlite3.connect(self.__dbPath, timeout=3000.00)
            cur = con.cursor()
            getCom = ("SELECT path, songDex, title, artist, album, duration FROM [%s]" % (self.skScrubName(name)))
            cur.execute(getCom)
            newList = cur.fetchall()
            for x in newList:
                skF = SKFile(x[0],x[1],x[2],x[3],x[4], x[5])
                retList.append(skF)   
            con.close()
            return retList
        except:
            return 1 #DB CONNECTION ERROR
        
    def skdbGetAll(self):
        '''
        Method for returning names of all tables in DB
        '''
        try:
            con = sqlite3.connect(self.__dbPath)
            cur = con.cursor()
            retList = []
            getCom = ("SELECT name FROM sqlite_master WHERE type='table';")
            vals = cur.execute(getCom)
            for x in vals:
                retList.append(x[0])
            con.close()
            return retList
        except:
            return 1 #DB CONNECTION ERROR
        
        
    def skdbSortList(self, option, name):
        '''
        Method for sorting a play list. Query the db for the proper table and sorting.
        Returns its content. Might be better to implement in GUI?
        
        NEEDS TO BE IMPLEMENTED (Or is it better to do this from GUI point of view?)
        '''
        if(option == 1):
            option = 'title'
        if(option == 2):
            option = 'artist'
        if(option == 3):
            option = 'album'
        try:
            con = sqlite3.connect(self.__dbPath)
            cur = con.cursor()
        except:
            return 1 #DB CONNECTION ERROR
        try:
            retList = []
            getCom = 'SELECT * FROM [' + self.skScrubName(name) + '] ORDER BY ' + option
            cur.execute(getCom)
            newList = cur.fetchall()
            for x in newList:
                skF = SKFile(x[0],x[1],x[2],x[3],x[4], x[5])
                retList.append(skF)
            return retList
        except:
            return 1
        
                
    def skdbNewList(self, name):
        '''
        Creates a new table in the database for a new play list.
        '''
        try:
            con = sqlite3.connect(self.__dbPath)
            cur = con.cursor()
        except:
            return 1 #DB CONNECTION ERROR
        tableD = """
        CREATE TABLE IF NOT EXISTS [%s] (
            path text UNIQUE NOT NULL,
            songDex integer PRIMARY KEY,
            title text,
            artist text,
            album text,
            duration integer
            )""" % (self.skScrubName(name))
        try:
            cur.execute(tableD)
            con.commit()
            con.close()
            return 0
        except:
            return 1

    def skdbRemoveList(self, name):
        '''
        Removes a table from the database
        
        UPDATE: Change name to be a variable, do not allow for SQL Injection
        '''
        try:
            con = sqlite3.connect(self.__dbPath)
            cur = con.cursor()
        except:
            return 1 #DB CONNECTION ERROR
        rmCom = ("DROP TABLE IF EXISTS [%s]" % (self.skScrubName(name)))
        try:
            cur.execute(rmCom)
            con.commit()
            con.close()
            return 0
        except:
            return 1
        
    def skdbUpdateList(self, op, name, skF):
        '''
        Method to add or remove a song from a table.
        op = add (1) or delete (anything else)
        name = play list name. Since they are chosen via selection, shouldn't run into not finding that list
        
        UPDATE: Change name to be a variable, do not allow for SQL Injection
        '''
        try:
            con = sqlite3.connect(self.__dbPath)
            cur = con.cursor()
        except:
            return 1 #DB CONNECTION ERROR
        #Adding to list
        if(op == 1):
            try:
                addTo = "INSERT INTO [%s] (path, songDex, title, artist, album, duration) VALUES (?,?,?,?,?,?)" % (self.skScrubName(name))
                cur.execute(addTo, (skF.path, skF.index, skF.title, skF.artist, skF.album, skF.time))
                con.commit()
                con.close()
                return 0
            except:
                return 1
        else:
            try:
#                 rmFrom = "DELETE FROM " + name + " WHERE songDex (index) VALUES (?)"
                index = str(skF.index)
                remTo = "DELETE FROM [%s] WHERE songDex=?;" % (self.skScrubName(name))
                cur.execute(remTo, (index))
                con.commit()
                con.close()
                return 0
            except:
                return 1
            
    def skdbUpdateListMany(self, op, name, items):
        '''
        Method to update a table with a list of entries. Either adding or removing. 
        UPDATE: Change name to be a variable, do not allow for SQL Injection
        '''
        try:
            con = sqlite3.connect(self.__dbPath)
            cur = con.cursor()
        except:
            return 1 #DB CONNECTION ERROR
        #Adding to list
        if(op == 1):
#             try:
            itemList = []
            for x in items:
                itemList.append([x.path, x.index, x.title, x.artist, x.album, x.time ])
            addTo = "INSERT OR IGNORE INTO [%s] (path, songDex, title, artist, album, duration) VALUES (?,?,?,?,?,?)" %(self.skScrubName(name))
            cur.executemany(addTo, (itemList))
            con.commit()
            con.close()
#             except:
#                 return 0
        else:
            try:
                itemList = []
                for x in items:
                    itemList.append([str(x.index)])
                rem = "DELETE FROM [%s] WHERE songDex=?;" % (self.skScrubName(name))
                cur.executemany(rem,(itemList))
                con.commit()
                con.close()
            except Exception as e:
                print(e)
                return 1
         
    def skdbUpdateDefault(self, content):
        '''
        Method that updates the default directory table from the sever.
        Holds an old table in case of issues, or programming in option to
        try and find new paths for play lists.
        '''
        
        #Check if table already exists, if so creade old default for backup
        try:
            con = sqlite3.connect(self.__dbPath)
            cur = con.cursor()
        except:
            return 1
#         try:
        findTable = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='defPlaylist'"
        cur.execute(findTable)
        valCheck = cur.fetchone()
        if(valCheck[0]>0):
            rmTable = "DROP TABLE IF EXISTS _defPlaylist_OLD"
            cur.execute(rmTable)   
            altTable = "ALTER TABLE defPlaylist RENAME TO _defPlaylist_OLD"
            cur.execute(altTable)
            rmTable = "DROP TABLE IF EXISTS defPlaylist"
            cur.execute(rmTable)    
#         except:
#             return 0
        tableD = """
        CREATE TABLE IF NOT EXISTS defPlaylist (
            path text UNIQUE NOT NULL,
            songDex integer PRIMARY KEY,
            title text,
            artist text,
            album text,
            duration integer
            )"""
        cur.execute(tableD)
        inCom = "INSERT INTO defPlaylist (path, songDex, title, artist, album, duration) VALUES (?,?,?,?,?,?)"
        for x in content:
            cur.execute(inCom, (x.path, x.index, x.title, x.artist, x.album, x.time))
        cur.execute("SELECT path, songDex, title, artist, album, duration FROM defPlaylist")
        tmplist = cur.fetchall()
        self.__list = []
        for x in tmplist:
            skF = SKFile(x[0],x[1],x[2],x[3],x[4], x[5])
            self.__list.append(skF)
        con.commit()
        con.close()
        return 1

    def skdbSearchList(self, option, value, list):
        if (option == 1):
            option = 'title'
        if (option == 2):
            option = 'artist'
        if (option == 3):
            option = 'album'
        try:
            con = sqlite3.connect(self.__dbPath)
            cur = con.cursor()
        except:
            return 1  # DB CONNECTION ERROR
        try:
            retList = []
            getCom = "SELECT * FROM [%s] WHERE [%s]=?;" % (self.skScrubName(list),option)
            cur.execute(getCom, value)
            newList = cur.fetchall()
            for x in newList:
                skF = SKFile(x[0], x[1], x[2], x[3], x[4], x[5])
                retList.append(skF)
            return retList
        except Exception as e:
            print(e)
            return 1

    def skdbGetUniques(self, option):
        try:
            con = sqlite3.connect(self.__dbPath)
            cur = con.cursor()
        except:
            return 1  # DB CONNECTION ERROR
        try:
            retList = []
            if option=='artist':
                getCom = "SELECT DISTINCT artist FROM defPlaylist"
            elif option=='album':
                getCom = "SELECT DISTINCT album FROM defPlaylist"
            cur.execute(getCom)
            newList = cur.fetchall()
            return newList
        except Exception as e:
            print(e)
            return 1

if __name__ == "__main__":
    s = 'HELLO W@RLD 19 !!))' 
    s = re.sub('[^0-9a-zA-Z ]+','',s)
    print(s)