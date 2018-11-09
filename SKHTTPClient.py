'''
Created on Sep 6, 2018

@author: C
'''
import struct
import requests
from pip._vendor.distlib.compat import raw_input
import os
from SKFile import SKFile


class SKHTTPClient(object):
    '''
    This class should handle all communications for the client application.
    The client GUI will call methods from here to properly run. The main method here will
    run a command line based application that should have full functionality
    '''

    def __init__(self, port, ip):
        '''
        SKCLient will be built with several methods all revolving the socket initialized within
        the constructor. (Unless a higher level communication method is chosen, further
        research is needed).

        port: network port to operate on
        ip: IP address of the server to contact
        path: location where sound files are held
        dir: String list of files on server
        dirPath: Path of client song directory
        sockStat: Status of if connection is open or not
        skFiles: List of songs in skFile format
        admPass: Password for admin connection
        cacheMax: Maximum number of songs held in cache specified by user
        '''
        self.__hostname = ip
        self.__port = port
        self.__dir = []
        self.__url = 'http://' + ip + ':' + str(port)
        self.__dirname = os.getcwd()
        self.__dirPath = os.path.join(self.__dirname, 'batches')
        if not os.path.isdir(self.__dirPath):
            os.makedirs(self.__dirPath)
        self.__skFiles = []
        # self.__admpass = 'None'
        self.__serveriplist = []
        self.__pubStats = []  # files had, files served, unique connections made
        self.__batchfiles = []  # Will contain batch downloads


    #
    # def setDir(self, path):
    #     self.__dirPath = path

    def skGetFileDir(self):
        return self.__skFiles

    def skSetIPHOST(self, host, port):
        '''
        Method for changing the connection settings of the client.
        '''
        self.__hostname = host
        self.__port = port

    def skTestConnection(self):
        '''
        Method for testing if connection is valid
        '''
        try:
            r = requests.head(self.__url)
            return 0
        except Exception:
            return 1

    def skBuildDir(self):
        '''Method that retrieves directory file from server and builds the skFiles array'''
        r = requests.get(self.__url + '/ls')
        try:
            with open("serverdirectory.txt", "wb") as text_file:
                text_file.write(r.content)
        except Exception:
            return 1
        try:
            with open("serverdirectory.txt", 'r') as text_file:
                self.__dir = text_file.readlines()
        except Exception as e:
            return 1
        self.__dir.pop()
        self.__skFiles = []
        for x in self.__dir:
            skFData = x.split('&%&')
            skf = SKFile(skFData[0], skFData[1], skFData[2], skFData[3], skFData[4], skFData[5])
            self.__skFiles.append(skf)
        return 0

    def skBatchFiles(self, list, folder):
        '''Method should download a list of files for later playback.'''


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

        if (command == 'update'):
            val = self.skBuildDir()
            if(val == 0):
                return  0
            else:
                return 1
        elif (command == 'ls'):
            i = 0
            for x in self.__dir:
                print((str(i) + ': ' + x).encode().decode())
                i += 1
        elif (command == 'file'):
            val = self.skOpen()
            if (val == 1):
                print("Error Contacting Server")
                return 1
            index = raw_input("Enter index: ")
            self.skGUIFILE(index)
            self.skClose()
        elif (command == 'admin'):
            command = raw_input('Enter Command')
            option = raw_input('Enter Option(s)')
            self.skAdminComm(command, option, option2)
            return
        elif (command == 'stats'):
            val = self.skOpen()
            if (val == 1):
                print("Error Contacting Server")
                return 1
            self.skSend('stats'.encode())
            data = self.skRCV().decode()
            self.__pubStats = []
            tempStats = data.split('&%&')  # files had, served, conns made
            tempStats.pop()
            for x in tempStats:
                print(x)
                self.__pubStats.append(int(x))
        #             print(self.__pubStats)
        elif (command == 'exit'):
            self.skCleanUp()
            sys.exit()  # REMOVE LATER

    def skAdminComm(self, command, option, option2):
        '''
        Method for handling admin tasks on server through client. Currently needs better password authentication
        should handle basic tasks for changing server settings

        'dir': User wants to change the server directory
        'close': User wants to shut down the server
        'port': User wants to change the operating port (requires restart)
        'stats': User wants to see advanced statistics about server
        'MULTI': Later command to support changing multiple options of server before reset. GUI specific NOT IMPLEMENTED
        '''
        val = self.skOpen()
        if (val == 1):
            print("Error Contacting Server")
            return 1
        self.skSend('admin'.encode())
        conf = self.skRCV()
        if (conf.decode() == 'authtoken'):
            self.skSend(self.__admpass.encode())
            conf = self.skRCV()
            if (conf.decode() == 'no'):
                '''Bad Password'''
                return 1
            elif (conf.decode() == 'yes'):
                if (command == 'exit'):
                    self.skSend('exit'.encode())
                    self.skClose()
                    return 0
                elif (command == 'reset'):
                    self.skSend('reset'.encode())
                    self.skClose()
                    return 0
                elif (command == 'settings'):
                    self.skSend(('settings%&' + option + '&%&' + option2).encode())
                    self.skClose()
                    self.__port = int(option)
                    return 0
                elif (command == 'dir'):
                    self.skSend('dir'.encode())
                    self.skClose()
                    return 0
                elif (command == 'stats'):
                    self.skSend('stats'.encode())
                    data = self.skRCV()
                    tempList = data.decode()
                    self.__serveriplist = tempList.split(',')
                    self.__serveriplist.pop()
                    self.skClose()
                    #                     print(self.__serveriplist) POSSIBLE EXTRA INDEX
                    return 0
                else:
                    self.skSend('error'.encode())
                    self.skClose()
                    return 0

    def skCleanUp(self):
        for x in self.__cache:
            try:
                os.remove(self.__skFiles[x].cachePath)
            except:
                pass


if __name__ == "__main__":
    ClientK = SKHTTPClient(65535, '184.75.148.148')
    ClientK.skUserComm('update')
    print(ClientK.skGetFileDir())

        # command = raw_input("Enter Command")
#         ClientK.connecter()
#         ClientK.trueSend("'Pridemoor Keep' Shovel Knight Remix-k3IKgJUTjlM.mp3".encode())
#         ClientK.commSwitch2("'Pridemoor Keep' Shovel Knight Remix-k3IKgJUTjlM.mp3")
#         print('done')
#         break
