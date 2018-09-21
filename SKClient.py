'''
Created on Sep 6, 2018

@author: C
'''
from _socket import SOCK_STREAM, AF_INET, socket
import struct
from pip._vendor.distlib.compat import raw_input

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
        
    def setDir(self, path):
        self.__dirPath = path
        
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
        self.__CS.connect((self.__hostname, self.__port))
        
    def skClose(self):
        '''
        Method for disconnecting client from the server, used either in shutdown or changing 
        ip/port., 
        '''
        
        self.__CS.close()
        
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
    
    def skRCVFile(self, name):
        '''
        Method for handling file transfer from server on request from server. This method handles name entries.
        '''
        self.skSend(name.encode())
        fileData = self.skRCV()
        #print(len(fileData))
        file = open(self.__dirPath + name, 'wb+')        
        file.write(fileData);
        file.close();
        return 1
    
    def skRCVFileIndex(self,index):
        name = self.__dir[index]
        self.skSend(name.encode())
        fileData = self.skRCV()
        #print(len(fileData))
        file = open(self.__dirPath + name, 'wb+')        
        file.write(fileData);
        file.close();
        return 1
    
    def comLine(self):
        '''
        Method that runs the client as a command line application. Takes in user input and
        passes it on.
        '''
        
        command = raw_input('Enter Command: ')
        self.comSwitch(command)
        
        
    def comSwitch(self, command):
        '''
        Method that takes in client input and passes it to the proper command
        
        command: user given message on command line
        'file': user is going to ask for a file
        'index': user is asking for a file by index
        'update': user is asking for directory update
        'ls': User is asking for directory display
        'path': User wants to change dl directory? (temp files will be removed after they reach a certain index)
        '''
        
        if(command=='update'):
            self.skOpen()
            self.skSend('ls'.encode())
            data = self.skRCV().decode()
            self.__dir = data.split('\n')
            self.__dir.pop()
            self.skClose()
        if(command == 'ls'):
            i=0
            for x in self.__dir:
                print(str(i) + ': ' + x)
                i+=1
        if(command == 'file'):
            self.skOpen()
            name = raw_input("Enter name: ")
            self.skSend('file'.encode())
            answerData = self.skRCV();
            answer = answerData.decode()
            if(answer == 'okay'):
                self.skRCVFile(name)
            else:
                print("No beuno")
            self.skClose()
        if(command == 'index'):
            self.skOpen()
            name = raw_input("Enter index: ")
            self.skSend('file'.encode())
            answerData = self.skRCV();
            answer = answerData.decode()
            if(answer == 'okay'):
                self.skRCVFileIndex(int(name))
            else:
                print("No beuno")
            self.skClose()

if __name__ == "__main__":
    port = raw_input("Enter port:  ")
    ip = raw_input("Enter IP:  ")
    path = raw_input("Enter file directory path:  ")

    if(port == 'default'):
        ClientK = SKClient("C:\\SoundFiles\\Client\\", 1445, '127.0.0.1');
    else:
        ClientK = SKClient(path,port,ip)
    #ClientK.connecter()
    while True:
        command = raw_input("Enter command: ")
        ClientK.comSwitch(command);
        #command = raw_input("Enter Command")
#         ClientK.connecter()
#         ClientK.trueSend("'Pridemoor Keep' Shovel Knight Remix-k3IKgJUTjlM.mp3".encode())
#         ClientK.commSwitch2("'Pridemoor Keep' Shovel Knight Remix-k3IKgJUTjlM.mp3")
#         print('done')
#         break
        