'''
Created on Sep 6, 2018

@author: C
'''
from _socket import SOCK_STREAM, AF_INET, socket
import struct
from pip._vendor.distlib.compat import raw_input
import os
from SKFile import SKFile
import sys #REMOVE LATER

class SKClient(object):
    '''
    This class should handle all communications for the client application. 
    The client GUI will call methods from here to properly run. The main method here will
    run a command line based application that should have full functionality
    '''


    def __init__(self, path, port, ip):
        '''
        SKCLient will be built with several methods all revolving the socket initialized within
        the constructor. (Unless a higher level communication method is chosen, further
        research is needed).
        
        port: network port to operate on
        ip: IP address of the server to contact
        path: location where sound files are held
        '''
        self.__CS = socket(AF_INET,SOCK_STREAM)
        self.__hostname = ip
        self.__port = port
        self.__dir = []
        self.__dirPath = path
        self.__playIndex = []
        self.__sockStat = False
        self.__skFiles = []
        self.__admpass = 'None'
#         self.skSetup()
          
    def skWriteSKC(self):
        '''
        Method that writes the updated directory list to the setup file.
        Will be phased out for database version.
        '''
        
        dirName = os.path.dirname(os.path.realpath(__file__))
        statPath = os.path.join(dirName, 'stat')
        with open(statPath + '\\skcfl18.sk','w',encoding='utf-8') as f:
            for x in self.__dir:
                f.write("%s\n" % x)
                            
    def setDir(self, path):
        self.__dirPath = path
        
    def skGetDir(self):
        return self.__skFiles
    
    def skGetPath(self):
        return self.__dirPath
        
    def skSetIPHOST(self, host, port):
        '''
        Method for changing the connection settings of the client.
        '''
        self.__hostname = host
        self.__port = port
        
    def skOpen(self):
        '''
        Method for connecting client to the server with a user defined ip/port
        
        port: network port to operate on
        ip: IP address of the server to contact
        '''
        
        self.__CS = socket(AF_INET,SOCK_STREAM)
#         self.__CS.settimeout(200)
        try:
            self.__CS.connect((self.__hostname, self.__port))
            self.__sockStat = True
            return 0
        except:
            return 1

        
    def skClose(self):
        '''
        Method for disconnecting client from the server, used either in shutdown or changing 
        ip/port., 
        '''
        
        self.__CS.close()
        self.__sockStat = False
        
    def skSend(self, data):
        '''
        skSend will be the main method of sending information to the server. Be it a command or filename.
        By using data size as a prefix, a send all command can be used.
        
        data: data to be sent
        '''
        
        data = struct.pack('>I', len(data)) + data
        self.__CS.sendall(data) 
        
    def skRCV(self):
        '''
        skRCV will handle taking packets from the server and appropriately pass the data. only
        used if data size is a prefix.
        '''
        rawSize = self.skRCVALL(4)
        if not rawSize:
            return None #Fix this to incorporate retries
        dataSize = struct.unpack('>I', rawSize)[0]
        return self.skRCVALL(dataSize)
    
    def skRCVALL(self, length):
        '''
        Helper function for receiving all the data specified by the length. Used after skRCV
        
        length: number of bytes to receive
        '''
        data = b''
        while len(data) < length:
            packet = self.__CS.recv(length - len(data))
            if not packet:
                return None #Fix for multiple tries
            data += packet
        return data
    
    def skGUIFILE(self, index):
        '''
        Method for GUI to prep server for index request
        '''
        connected = self.skOpen()
        if(connected == 0):
            self.skSend('file'.encode())
            answerData = self.skRCV();
            if answerData:
                answer = answerData.decode()
                if(answer == 'okay'):
                    return self.skRCVFileIndex2(index)
                else:
                    return 0
            else:
                return 0
            self.skClose()
            
    def skRCVFileIndex2(self,index):
        '''
        Method for handling file transfer from server on request from server. This method handles index entries.
        
        index: Number of file to download
        '''
        
        if not self.__sockStat:
            self.skOpen()
        self.skSend(str(index).encode())
        fileData = self.skRCV()
        try:
            name = self.__skFiles[index].path
        except:
            return 0
        if fileData:
            if not os.path.exists(os.path.dirname(self.__dirPath + name)):
                try:
                    os.makedirs(os.path.dirname(self.__dirPath + name))
                except Exception as e:
                    print(e)
                    return 0
            file = open(self.__dirPath + name, 'wb+')        
            file.write(fileData);
            file.close();
            return 1
        else:
            return 0
        
        if self.__sockStat:
            self.skClose()
        
    def skUserComm(self, command):
        '''
        Method that takes in client input and passes it to the proper command
        
        command: user given message on command line
        'file': user is going to ask for a file
        'index': user is asking for a file by index
        'update': user is asking for directory update
        'ls': User is asking for directory display (Can cause crash in non-gui mode, fixable but I'm lazy & uneccesary)
        'stats': User wants to see stats about server
        '''
        
        if(command=='update'):
            val = self.skOpen()
            if(val == 1):
                print("Error Contacting Server")
                return 1
            self.skSend('ls'.encode())
            data = self.skRCV().decode()
            self.__dir = data.split('\n')
            self.__dir.pop()
            self.__skFiles = []
            for x in self.__dir:
                skFData = x.split('&%&')
                skf = SKFile(skFData[0],skFData[1],skFData[2],skFData[3],skFData[4])
                self.__skFiles.append(skf)
            self.skClose()
            self.skWriteSKC()
        if(command == 'ls'):
            i=0
            for x in self.__dir:
                print((str(i) + ': ' + x).encode().decode())
                i+=1
        if(command == 'file'):
            val = self.skOpen()
            if(val == 1):
                print("Error Contacting Server")
                return 1
            index = raw_input("Enter index: ")
            self.skGUIFILE(index)
            self.skClose()
        if(command == 'admin'):
            command2 = raw_input('Enter Command')
            option = raw_input('Enter Option')
            self.skAdminComm(command2, option)
        if(command=='exit'):
            sys.exit() #REMOVE LATER

                       
    def skAdminComm(self, command, option):
        '''
        Method for handling admin tasks on server through client. Currently needs better password authentication
        should handle basic tasks for changing server settings
        
        'dir': User wants to change the server directory
        'close': User wants to shut down the server
        'port': User wants to change the operating port (requires restart)
        'stats': User wants to see advanced statistics about server
        '''
        val = self.skOpen()
        if(val == 1):
            print("Error Contacting Server")
            return 1
        self.skSend('admin'.encode())
        conf = self.skRCV()
        if(conf.decode()=='authtoken'):
            self.skSend(self.__admpass.encode())
            conf = self.skRCV()
            if(conf.decode()=='no'):
                '''Bad Password'''
                return 1
            elif(conf.decode()=='yes'):
                if(command == 'exit'):
                    self.skSend('exit'.encode())
                    self.skClose()
                    return 0
                if(command == 'reset'):
                    self.skSend('reset'.encode())
                    self.skClose()
                    return 0
                if(command == 'port'):
                    self.skSend(('port&%&'+option).encode())
                    self.skClose()
                    self.__port = int(option)
                    return 0
                else:
                    self.skSend('error'.encode())
                    self.skClose()
                    return 0
        
if __name__ == "__main__":
    port = raw_input("Enter port:  ")
    if(port!='default'):
        port = int(port)
        ip = raw_input("Enter IP:  ")
        path = raw_input("Enter file directory path:  ")

    if(port == 'default'):
        ClientK = SKClient("C:\\SoundFiles\\Client\\", 65535, '184.75.148.148');
    else:
        ClientK = SKClient(path,port,ip)
    #ClientK.connecter()
    while True:
        command = raw_input("Enter command: ")
        ClientK.skUserComm(command);
        #command = raw_input("Enter Command")
#         ClientK.connecter()
#         ClientK.trueSend("'Pridemoor Keep' Shovel Knight Remix-k3IKgJUTjlM.mp3".encode())
#         ClientK.commSwitch2("'Pridemoor Keep' Shovel Knight Remix-k3IKgJUTjlM.mp3")
#         print('done')
#         break
        