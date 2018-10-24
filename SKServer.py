'''
Created on Sep 7, 2018

@author: C
'''

from _socket import SOCK_STREAM, AF_INET, gethostname
import socket
import threading
import os
import struct
from pip._vendor.distlib.compat import raw_input
from tinytag import TinyTag
from SKFile import SKFile
import configparser
import signal
import sys
from _thread import interrupt_main



class ExitSignal(Exception):
    pass

class SKServer(object):
    '''
    This class is to be the server that hands out music files to the requesting client.
    Both a command line interface and simple UI should be options for running.
    '''


    def __init__(self):
        '''
        Constructor sets up server socket address/port, the default directory, and the
        number of connections the server will handle at once.
        
        port: the port the server will operate on
        path: default directory
        connections: Max number of connections serviceable at one time.
        password: Auth token to be present in all received communication. Without it, the request is ignored.
        skFiles: List of all songs in SKFile format.
        dir: list of all songs in string format (For sending to client, probably not needed since skfiles have
         this capability)
        '''
        self.__SS = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0);
        self.__hostname = socket.gethostbyname(gethostname())
        self.skSetup()
        self.__SS.bind((self.__hostname,self.__port));
        #os.chdir(path)
        self.__skFiles = []
        self.__dir = self.skSetDir(self.__path);
        self.__filesServed = 0;
        
    def skClose(self, cs):
        '''
        Method that closes server from an informing thread. Makes use of a seccond connection attempt to
        raise an error in the main listening loop to escape.
        '''
        self.skUpdateINI()
        cs.close()
        socket.socket(socket.AF_INET,socket.SOCK_STREAM).connect((self.__hostname,self.__port))
        self.__SS.close()
        print('Goodbye')
        
    def skSetup(self):
        '''
        Method for reading the ini file provided to the server
        
        UPDATE: PATH CHECKING
        '''
        #Ensure path is correct
        dirName = os.path.dirname(os.path.realpath(__file__))
        if(os.path.isfile('settings.ini')):
            #Process ini file
            try:
                config = configparser.ConfigParser()
                config.read('settings.ini')
                self.__port = int(config['DEFAULT']['ServerPort'])
                self.__conns = int(config['DEFAULT']['ConnectionLimit'])
                self.__pass = config['DEFAULT']['ConnectionPassword']
                self.__admPass = config['DEFAULT']['AdminPassword']
                self.__path = config['DEFAULT']['ServerDirectory']
            except:
                print('Issue reading ini file')
                os.rename('settings.ini', 'settings.ini.bak', src_dir_fd=None, dst_dir_fd=None)
                self.skSetup
        else:
            try:
                config = configparser.ConfigParser()
                self.__port = int(raw_input("Enter server port:  "))
                self.__conns = int(raw_input("Enter max number of connections:  "))
                self.__pass = raw_input("Enter connection password:  ")
                self.__admPass = raw_input("Enter admin control password:  ")
                self.__path = raw_input("Enter file directory path:  ")
                if(not self.__path.endswith('\\')):
                        self.__path.append('\\')
                config['DEFAULT'] = {}
                config['DEFAULT']['ServerPort'] = str(self.__port)
                config['DEFAULT']['ConnectionLimit'] = str(self.__conns)
                config['DEFAULT']['ConnectionPassword'] = self.__pass
                config['DEFAULT']['AdminPassword'] = self.__admPass
                config['DEFAULT']['ServerDirectory'] = self.__path
                with open('settings.ini', 'w') as iniFile:
                    config.write(iniFile)
            except:
                print('Error making ini file')
            #Make new ini

    def skUpdateINI(self):
        try:
            config = configparser.ConfigParser()
            config['DEFAULT'] = {}
            config['DEFAULT']['ServerPort'] = str(self.__port)
            config['DEFAULT']['ConnectionLimit'] = str(self.__conns)
            config['DEFAULT']['ConnectionPassword'] = self.__pass
            config['DEFAULT']['AdminPassword'] = self.__admPass
            config['DEFAULT']['ServerDirectory'] = self.__path
            with open('settings.ini', 'w') as iniFile:
                config.write(iniFile)
        except:
            print('Error making ini file')
            
    def skListen(self):
        '''
        Main method of running the server, allowing connections from clients. Opens
        the server sockets and starts individual threads based on requests.
        '''
        try:
            self.__SS.listen(self.__conns)
            print('Server listening on port: ' + str(self.__port))
            while(True):
                CS,CS_Addr = self.__SS.accept();
                CS.settimeout(200)
                threading.Thread(target = self.skClientDist, args = (CS, CS_Addr)).start()
        except socket.error:
            print('Closing Server')
            return 0
        
    def skClientDist(self,cs,csAddr):
        '''
        Thread method for handling single connections to clients. If a selector option is used, will
        have to be modified. For now kicks a connection once a command is processed.
        
        cs: socket connection to specific client
        csAddr: address of the client that has connected.
        '''
        print("Connection established with " + str(csAddr))
        commData = self.skRCV(cs)
        while not commData:
            commData = self.skRCV(cs)
        comm = commData.decode()
        self.skClientComm(comm,cs)   
        cs.close()
            
        
        
    def skSend(self, data, socket):
        '''
        skSend will be the main method of sending information to the server. Be it a command or filename.
        By using data size as a prefix, a send all command can be used.
        
        data: data to be sent
        socket: connection data is sent on
        '''
        
        data = struct.pack('>I', len(data)) + data
        socket.sendall(data) 
        
    def skRCV(self,socket):
        '''
        skRCV will handle taking packets from the server and appropriately pass the data. only
        used if data size is a prefix. Works in tandem with skRCVALL
        
        socket: connection to receive on
        '''
        rawSize = self.skRCVALL(socket, 4)
        if not rawSize:
            return None #Fix this to incorporate retries
        dataSize = struct.unpack('>I', rawSize)[0]
        return self.skRCVALL(socket, dataSize)
    
    def skRCVALL(self,socket, length):
        '''
        Helper function for receiving all the data specified by the length. Used after skRCV
        
        socket: connection to receive on
        length: number of bytes to receive
        '''
        data = b''
        while len(data) < length:
            packet = socket.recv(length - len(data))
            if not packet:
                return None #Fix for multiple tries
            data += packet
            return data
    
    def skAdminComm(self, socket):
        '''
        Method that takes in user input and passes it to the proper command
        
        command: user given message on command line
        'port': User is changing the port of the server.
        'exit': User is shutting down server.
        'reset': User is resetting the server.
        'dir': User is changing/deleting/adding directory.
        UNIMPLEMENTED
        '''
        self.skSend('authtoken'.encode(), socket)
        auth = self.skRCV(socket)
        if(auth.decode()!=self.__admPass):
            print('Unauthorized Token Attempt')
            self.skSend('no'.encode(), socket)
            return 1
        self.skSend('yes'.encode(), socket)
        commData = self.skRCV(socket)
        command = commData.decode().split('&%&')
        if(command[0]=='port'):
            'Change port, requires reset'
        if(command[0]=='reset'):
            'reset server'
        if(command[0]=='exit'):
            'close server'
            self.skClose(socket)
        
    def skClientComm(self, command, socket):
        '''
        Method that takes in client input and passes it to the proper command
        
        socket: connection to interact with
        command: user given message on command line
        'ls': client is requesting directory map
        'file' client is requesting a file
        'admin' client is requesting admin console request (password auth?)
        '''
        
        if(command == 'ls'):
            self.skSend(self.__dir.encode(), socket)
        if(command == 'file'):
            self.skSend('okay'.encode(), socket)
            nameData = self.skRCV(socket)
            filepath = nameData.decode()
            print(filepath)
            filepath = self.__skFiles[int(filepath)].path
            self.skFileDist(filepath, socket)
        if(command == 'admin'):
            self.skAdminComm(socket);
     
    def skSetDir(self,path):
        '''
        Method that sets the directory for the server to use. Future iterations should support
        multiple directories. This method is OS based and is assuming the user is on Windows
        
        path: The location of the directory to be used.
        '''
        os.chdir(path)
        #fileArr = os.listdir(path)
        retArr2 = ""
        self.__skFiles = []
        self.__errList = []

        i = 0
        for root, dirs, files in os.walk('.'):
            for name in files:
                if(root == '.'):
                    #Tiny Tag supports other formats, but for now mp3 will suffice
                    if(name.endswith('.mp3')):
                        try:
#                             sys.stdout.buffer.write((name+'\n').encode())
                            tag = TinyTag.get(name)
                            skF = SKFile(name,i,tag.title,tag.artist,tag.album)
                            i+=1
                            self.__skFiles.append(skF)
                        #Special duration error on TinyTag Most likely Throws 2 errors
                        except Exception as e:
                            try:
                                tag = TinyTag.get(name, duration=False)
                                skF = SKFile(name,i,tag.title,tag.artist,tag.album)
                                i+=1
                                self.__skFiles.append(skF)
                            #Second TinyTag failure, give up on that file
                            except:
                                self.__errList.append(name)
                                pass
                else:
                    if(name.endswith('.mp3')):
                        newRoot = root[2:] + '\\' + name
                        try:
                            tag = TinyTag.get(newRoot)
                            skF = SKFile(newRoot,i,tag.title,tag.artist,tag.album)
                            i+=1
                            self.__skFiles.append(skF)
                        except:
                            try:
                                tag = TinyTag.get(newRoot, duration=False)
                                skF = SKFile(newRoot,i,tag.title,tag.artist,tag.album)
                                i+=1
                                self.__skFiles.append(skF)
                            except:
                                self.__errList.append(name)
                                pass
        for x in self.__skFiles:
            retArr2 = retArr2 + x.skToString() + '\n'
#         for x in self.__errList:
#             sys.stdout.buffer.write((x+'\n').encode())

        return retArr2
    
        
    def skFileDist(self, filepath, socket):
        '''
        Method that enables the server to take a file from its directory and send the 
        data to the client
        
        file path: name/location of the file to be sent.
        socket: connection to send file on. 
        '''
        try:
            #print(self.__path + filepath)
            fileSize = os.path.getsize(self.__path + filepath) #stat("C:\\SoundFiles\\Server\\lz.mp3")
            print(fileSize)
            file = open(self.__path + filepath,'rb')
            fileData = file.read(fileSize)
            file.close()
            print('Sending file')
            self.skSend(fileData, socket)
        except Exception as e:
            print(e)
            
            
if __name__ == "__main__":
    ServerK = SKServer();
    ServerK.skListen()
    print('Server Closed')