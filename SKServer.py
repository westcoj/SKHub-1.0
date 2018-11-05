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
        
        homeDir: Grabs the working directory for future use (os.chdir is used in directory walk, meaning we need a way to return)
        port: the port the server will operate on
        path: default directory
        connections: Max number of connections serviceable at one time.
        password: Auth token to be present in all received communication. Without it, the request is ignored.
        skFiles: List of all songs in SKFile format.
        dir: list of all songs in string format (For sending to client, probably not needed since skfiles have
         this capability)
        '''
        self.__homeDir = os.getcwd()
        self.__SS = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
        self.__SS.settimeout(5)
        self.__hostname = socket.gethostbyname(gethostname())
        self.__pubStats = [0,0,0]  #Files Had, Files Served, Unique Conns Made
        self.__ipList = []
        self.skSetup()
        self.__SS.bind((self.__hostname,self.__port));
        #os.chdir(path)
        self.__skFiles = []
        self.__dir = self.skSetDir(self.__path);
        self.__reset = 0
        self.__exitVal = 0
    
    def skReset(self):
        return self.__reset
        
    def skSetup(self):
        '''
        Method for reading the ini file provided to the server
        
        UPDATE: PATH CHECKING
        '''
        #Ensure path is correct
        os.chdir(self.__homeDir)
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
                self.__pubStats[1] = int(config['STATS']['FilesServed'])
                self.__pubStats[2] = int(config['STATS']['ConnectionsMade'])
                try:
                    self.__ipList = config['IPADDRS']['LIST'].split(',')
                except:
                    pass
            except Exception as e:
                print(e)
                if(os.path.isfile('settings.ini.bak')):
                    os.remove('settings.ini.bak')
                print('Issue reading ini file')
                os.rename('settings.ini', 'settings.ini.bak', src_dir_fd=None, dst_dir_fd=None)
                self.skSetup()
        else:
#             try:
            config = configparser.ConfigParser()
            self.__port = int(raw_input("Enter server port:  "))
            self.__conns = int(raw_input("Enter max number of connections:  "))
            self.__pass = raw_input("Enter connection password:  ")
            self.__admPass = raw_input("Enter admin control password:  ")
            self.__path = raw_input("Enter file directory path:  ")
            if(not self.__path.endswith('\\')):
                    self.__path += '\\'
            config['DEFAULT'] = {}
            config['DEFAULT']['ServerPort'] = str(self.__port)
            config['DEFAULT']['ConnectionLimit'] = str(self.__conns)
            config['DEFAULT']['ConnectionPassword'] = self.__pass
            config['DEFAULT']['AdminPassword'] = self.__admPass
            config['DEFAULT']['ServerDirectory'] = self.__path
            config['STATS'] = {}
            config['STATS']['FilesServed'] = str(self.__pubStats[1])
            config['STATS']['ConnectionsMade'] = str(self.__pubStats[2])
            config['IPADDRS'] = {}
            ipstring = ''
            for x in self.__ipList:
                print(x)
                ipstring = ipstring + (str(x) +',')
            config['IPADDRS']['LIST'] = ipstring
            
            with open('settings.ini', 'w') as iniFile:
                config.write(iniFile)
#             except Exception as e:
#                 print(e)
#                 print('Error making ini file')

    def skUpdateINI(self):
        print(self.__ipList)
        os.chdir(self.__homeDir)
        try:
#             if(os.path.isfile('settings.ini')):
#                 os.remove('settings.ini')
            config = configparser.ConfigParser()
            config['DEFAULT'] = {}
            config['DEFAULT']['ServerPort'] = str(self.__port)
            config['DEFAULT']['ConnectionLimit'] = str(self.__conns)
            config['DEFAULT']['ConnectionPassword'] = self.__pass
            config['DEFAULT']['AdminPassword'] = self.__admPass
            config['DEFAULT']['ServerDirectory'] = self.__path
            config['STATS'] = {}
            config['STATS']['FilesServed'] = str(self.__pubStats[1])
            config['STATS']['ConnectionsMade'] = str(self.__pubStats[2])
            config['IPADDRS'] = {}
            ipstring = ''
            for x in self.__ipList:
                print(x)
                ipstring = ipstring + (str(x) +',')
            config['IPADDRS']['LIST'] = ipstring
            with open('settings.ini', 'w') as iniFile2:
                config.write(iniFile2)
                            
        except Exception as e:
            print(e)
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
                try:
                    CS,CS_Addr = self.__SS.accept();
                    addr = CS.getpeername()
                    print(addr[0])
                    if addr[0] not in self.__ipList:
                        self.__ipList.append(addr[0])
                        self.__pubStats[2] += 1
                    CS.settimeout(200)
                    threading.Thread(target = self.skClientDist, args = (CS, CS_Addr)).start()
                except socket.timeout:
                    if(self.__exitVal == 1):
                        self.__SS.close()
                        print(self.__port)
                        self.skUpdateINI()
                        print('Closing Server TRU')
                        return 0  
                except socket.error:
                    print('Closing Server')
                    return 0
        except Exception as e:
            print(e)
    
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
#         sys.exit()
        return
            
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
        if(command[0]=='settings'):
            'Change port, requires reset'
            portNum = int(command[1])
            connsNum = int(command[2])
            self.__port=portNum
            self.__conns=connsNum
            self.skUpdateINI()
            self.__reset = 1
            self.__exitVal = 1
            return
        elif(command[0]=='stats'):
            'send ip list'
            ipList = ''
            for x in self.__ipList:
                ipList += (str(x) + ',')
            self.skSend(ipList.encode(), socket)
            return
        elif(command[0]=='reset'):
            'reset server'
            self.__reset = 1
            self.__exitVal = 1
            return
        elif(command[0]=='exit'):
            'close server'
            self.__exitVal = 1
            return
        elif(command[0]=='multiple'):
            'parse changes'
        else:
            'error with command'
            print('Wrong Command')
            return

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
        if(command == 'stats'):
            '''Get Public Stats'''
            dataSend = ''
            for x in self.__pubStats:
                dataSend = dataSend + str(x) + '&%&'
            self.skSend(dataSend.encode(), socket)
        if(command == 'admin'):
            self.skAdminComm(socket);
        return
     
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
#                     sys.stdout.buffer.write((name+'\n').encode())
                    #Tiny Tag supports other formats, but for now mp3 will suffice
                    if(name.endswith('.mp3')):
                        try:
#                             sys.stdout.buffer.write((name+'\n').encode())
                            tag = TinyTag.get(name)
                            skF = SKFile(name,i,tag.title,tag.artist,tag.album)
                            i+=1
                            self.__skFiles.append(skF)
                            self.__pubStats[0] += 1
                        #Special duration error on TinyTag Most likely Throws 2 errors
                        except Exception as e:
                            try:
                                tag = TinyTag.get(name, duration=False)
                                skF = SKFile(name,i,tag.title,tag.artist,tag.album)
                                i+=1
                                self.__skFiles.append(skF)
                                self.__pubStats[0] += 1
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
                            self.__pubStats[0] += 1
                        except:
                            try:
                                tag = TinyTag.get(newRoot, duration=False)
                                skF = SKFile(newRoot,i,tag.title,tag.artist,tag.album)
                                i+=1
                                self.__skFiles.append(skF)
                                self.__pubStats[0] += 1
                            except:
                                self.__errList.append(name)
                                pass
        for x in self.__skFiles:
            retArr2 = retArr2 + x.skToString() + '\n'
#             sys.stdout.buffer.write((x.skToString()+'\n').encode())
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
            self.__pubStats[1] += 1
        except Exception as e:
            print(e)
            
            
if __name__ == "__main__":
    val = 1
    while(val==1):
        ServerK = SKServer();
        ServerK.skListen()
        val = ServerK.skReset()
    os._exit(0)