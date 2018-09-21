'''
Created on Sep 7, 2018

@author: C
'''

from _socket import SOCK_STREAM, AF_INET
from socket import socket
#from _thread import *
import threading
import os
import struct
from pip._vendor.distlib.compat import raw_input




class SKServer(object):
    '''
    This class is to be the server that hands out music files to the requesting client.
    Both a command line interface and simple UI should be options for running.
    '''


    def __init__(self, port, path, connections, password):
        '''
        Constructor sets up server socket address/port, the default directory, and the
        number of connections the server will handle at once.
        
        port: the port the server will operate on
        path: default directory
        connections: Max number of connections serviceable at one time.
        password: Auth token to be present in all received communication. Without it, the request is ignored.
        '''
        
        self.__SS = socket(AF_INET,SOCK_STREAM,0);
        self.__hostname = '127.0.0.1' #self.__SS.gethostname();
        self.__port = port;
        self.__SS.bind((self.__hostname,self.__port));
        self.__path = path;
        #os.chdir(path)
        self.__dir = self.skSetDir(path);
        self.__conns = connections;
        self.__pass = password;
        
    def skListen(self):
        '''
        Main method of running the server, allowing connections from clients. Opens
        the server sockets and starts individual threads based on requests.
        '''
        
        self.__SS.listen(self.__conns)
        while(True):
            CS,CS_Addr = self.__SS.accept();
            CS.settimeout(200)
            threading.Thread(target = self.skClientDist, args = (CS, CS_Addr)).start()
        
        
    def skClientDist(self,cs,csAddr):
        '''
        Thread method for handling single connections to clients. If a selector option is used, will
        have to be modified. For now kicks a connection once a command is processed.
        
        cs: socket connection to specific client
        csAddr: address of the client that has connected.
        '''
        print("Connection established...")
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
        used if data size is a prefix.
        
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
    
    def skUserComm(self, command):
        '''
        Method that takes in user input and passes it to the proper command
        
        command: user given message on command line
        'port': User is changing the port of the server.
        'exit': User is shutting down server.
        'reset': User is resetting the server.
        'dir': User is changing/deleting/adding directory.
        '''
        
        
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
            self.skFileDist(filepath, socket)
        
    def skSetDir(self,path):
        '''
        Method that sets the directory for the server to use. Future iterations should support
        multiple directories. This method is OS based and is assuming the user is on Windows
        
        path: The location of the directory to be used.
        '''
        os.chdir(path)
        fileArr = os.listdir(path)
        retArr = "";
        for x in fileArr:
            retArr = retArr + x
            retArr += "\n"
        return retArr
    
        
    def skFileDist(self, filepath, socket):
        '''
        Method that enables the server to take a file from its directory and send the 
        data to the client succesfully
        
        filepath: name/location of the file to be sent.
        socket: connection to send file on. 
        '''
        try:
            fileSize = os.path.getsize(self.__path + filepath) #stat("C:\\SoundFiles\\Server\\lz.mp3")
            print(fileSize)
            file = open(self.__path + filepath,'rb')
            fileData = file.read(fileSize)
            file.close()
            print('Sending file')
            self.skSend(fileData, socket)
        except:
            print("error")
            
            
if __name__ == "__main__":

    port = raw_input("Enter port:  ")
    path = raw_input("Enter file directory path:  ")
    pswd = raw_input("Enter password (unused function):  ")
    conn = int(raw_input("Enter number of connections:  "))

    if(port == 'default'):
        ServerK = SKServer(1445, 'C:\\SoundFiles\\Server\\', 5, 'FileServer');
    else:
        ServerK = SKServer(port, path,conn,pswd)
    ServerK.skListen()
    