'''
Created on Sep 21, 2018

@author: Cody
'''

import os
import random
from SKFile import SKFile
import sqlite3

class SKMedia(object):
    '''
    This class will support the operation of audio media for SKClient. It will handle 
    the distribution of files and play list management.
    '''


    def __init__(self):
        '''
        Constructor to set up media handler
        '''
        self.__list = [] 
        self.__cacheList = []
        self.__listIndex = 0
        self.__dirName = os.path.dirname(os.path.realpath(__file__))
        self.__plPath = os.path.join(self.__dirName, 'playlists')
        self.__dbPath = os.path.join(self.__dirName, 'playlists\\db.sqlite3')
        if not os.path.isdir(self.__plPath):
            os.makedirs(self.__plPath)
        #os.chdir(plPath)
        #self.skLoadList('default.pl')
        
    def skGetList(self):
        return self.__list
    
    def skLoadList(self, name):
        '''
        Method to load playlist, not implemented, current list is just a default
        '''
#         with open(name) as f:
#             self.__list = f.readlines()
        if os.path.isfile(self.__plPath + name):
            self.__list = []
            skfList = [line.rstrip('\n') for line in open(name,encoding='utf-8')]
            for x in skfList:
                skFData = x.split('&%&')
                skF = SKFile(skFData[0],skFData[1],skFData[2],skFData[3],skFData[4])
                self.__list.append(skF)
         
    def skShuffleList(self,list):
        '''
        Method for shuffling a list
        '''
        listCopy = list
        random.shuffle(listCopy)
        return listCopy
        
    def skSetList(self,content):
        '''
        Method for rewriting entire list (default only, update call)
        '''
        with open('default.pl', 'w',encoding = 'utf-8') as f:
            for x in content:
                f.write("%s\n" % x)
                
        self.__list = content
                
    def skTestList(self):
        for x in self.__list:
            print(x)
            
    #----------------------------------------DB METHODS-------------------------#
    
    def skdbGetList(self, name):
        '''
        Method for obtaining a table from the database and returning its contents
        '''
        newList = []
        retList = []
#         try:
        con = sqlite3.connect(self.__dbPath)
        cur = con.cursor()
        getCom = ("SELECT path, songDex, title, artist, album FROM %s" % (name))
        cur.execute(getCom)
        newList = cur.fetchall()
        for x in newList:
            skF = SKFile(x[0],x[1],x[2],x[3],x[4])
            retList.append(skF)
        return retList
#         except:
        return 0 #DB CONNECTION ERROR
        
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
            return retList
        except:
            return [0] #DB CONNECTION ERROR
        
        
    def skdbSortList(self, option, name):
        '''
        Method for sorting a playlist. Query the db for the proper table and sorting.
        Returns its content.
        '''
        
        try:
            con = sqlite3.connect(self.__dbPath)
            cur = con.cursor()
        except:
            return 0 #DB CONNECTION ERROR
        try:
            retList = []
            getCom = 'SELECT * FROM ' + name + ' ORDER BY ' + option
            cur.execute(getCom)
            newList = cur.fetchall()
            for x in newList:
                skF = SKFile(x[0],x[1],x[2],x[3],x[4])
                retList.append(skF)
            return retList
        except:
            return 0
        
                
    def skdbNewList(self, name):
        '''
        Creates a new table in the db for a new playlist.
        '''
        try:
            con = sqlite3.connect(self.__dbPath)
            cur = con.cursor()
        except:
            return 0 #DB CONNECTION ERROR
        tableD = """
        CREATE TABLE IF NOT EXISTS %s (
            path text UNIQUE NOT NULL,
            songDex integer PRIMARY KEY,
            title text,
            artist text,
            album text)""" % (name)
        try:
            cur.execute(tableD)
            con.commit()
            con.close()
            return 1
        except:
            return 0
        
    def skdbRemoveList(self, name):
        '''
        Removes a table from the db
        '''
        try:
            con = sqlite3.connect(self.__dbPath)
            cur = con.cursor()
        except:
            return 0 #DB CONNECTION ERROR
        rmCom = "DROP TABLE IF EXISTS " + name
        try:
            cur.execute(rmCom)
            con.commit()
            con.close()
            return 1
        except:
            return 0
        
    def skdbUpdateList(self, op, name, skF):
        '''
        Method to add or remove a song from a table.
        op = add (1) or delete(anything else)
        name = playlist name. Since they are chosen via selection, shouldn't run into not finding that list
        '''
        try:
            con = sqlite3.connect(self.__dbPath)
            cur = con.cursor()
        except:
            return 0 #DB CONNECTION ERROR
        #Adding to list
        if(op == 1):
            try:
                addTo = "INSERT INTO " + name + " (path, songDex, title, artist, album) VALUES (?,?,?,?,?)"
                cur.execute(addTo, (skF.path, skF.index, skF.title, skF.artist, skF.album))
                con.commit()
                con.close()
            except:
                return 0
        else:
            try:
                rmFrom = "DELETE FROM " + name + " WHERE songDex (index) VALUES (?)"
                index = str(skF.index)
                cur.execute("DELETE FROM " + name + " WHERE songDex=?",(index,))
                con.commit()
                con.close()
            except:
                return 0
            
    def skdbUpdateListMany(self, op, name, items):
        '''
        Method to update a table with a list of entries. Either adding or removing.
        '''
        try:
            con = sqlite3.connect(self.__dbPath)
            cur = con.cursor()
        except:
            return 0 #DB CONNECTION ERROR
        #Adding to list
        if(op == 1):
#             try:
            itemList = []
            for x in items:
                itemList.append([x.path, x.index, x.title, x.artist, x.album ])
            addTo = "INSERT OR IGNORE INTO " + name + " (path, songDex, title, artist, album) VALUES (?,?,?,?,?)"
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
                rem = "DELETE FROM " + name + " WHERE songDex=?;"
                cur.executemany(rem,(itemList))
                con.commit()
                con.close()
            except Exception as e:
                print(e)
                return 0
         
    def skdbUpdateDefault(self, content):
        '''
        Method that updates the default directory table from the sever.
        Holds an old table in case of issues, or programming in option to
        try and find new paths for playlists.
        '''
        
        #Check if table already exists, if so creade old default for backup
        try:
            con = sqlite3.connect(self.__dbPath)
            cur = con.cursor()
        except:
            return 0
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
            album text)"""
        cur.execute(tableD)
        inCom = "INSERT INTO defPlaylist (path, songDex, title, artist, album) VALUES (?,?,?,?,?)"
        for x in content:
            cur.execute(inCom, (x.path, x.index, x.title, x.artist, x.album))
        cur.execute("SELECT path, songDex, title, artist, album FROM defPlaylist")
        tmplist = cur.fetchall()
        self.__list = []
        for x in tmplist:
            skF = SKFile(x[0],x[1],x[2],x[3],x[4])
            self.__list.append(skF)
        con.commit()
        con.close()
        return 1
    
if __name__ == "__main__":
    skm = SKMedia()
    skm.skdbGetAll()