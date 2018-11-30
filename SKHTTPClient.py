'''
Created on Sep 6, 2018

@author: Cody
'''
import struct
import requests
from requests.auth import HTTPBasicAuth
from pip._vendor.distlib.compat import raw_input
import os
from SKFile import SKFile


class SKHTTPClient(object):
    '''
    This class should handle all communications for the client application.
    The client GUI will call methods from here to properly run. The main method here will
    run a command line based application that should have full functionality
    '''

    def __init__(self, port, ip, custom, timeout):
        '''
        SKCLient will be built with several methods all revolving the socket initialized within
        the constructor. (Unless a higher level communication method is chosen, further
        research is needed).

        port: network port to operate on
        ip: IP address of the server to contact
        path: location where sound files are held
        dir: String list of files on server
        dirPath: Path of client song directory
        skFiles: List of songs in skFile format
        admPass: Password for admin connection
        '''
        self.__hostname = ip
        self.__port = port
        self.__dir = []
        self.__url = 'http://' + self.__hostname + ':' + str(self.__port) + '/'
        self.__dirname = os.getcwd()
        self.__dirPath = os.path.join(self.__dirname, 'batches')
        if not os.path.isdir(self.__dirPath):
            os.makedirs(self.__dirPath)
        self.__skFiles = []
        self.__serveriplist = []
        self.__pubStats = []  # files had, files served, unique connections made
        self.__batchfiles = []  # Will contain batch downloads
        self.__customServer = custom
        self.__timeout = timeout

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
            r = requests.head((self.__url + 'hello'), timeout=self.__timeout)
            return 0 #Connection exists
        except requests.RequestException:
            return 1 #No connection

    def skCheckFile(self, index):
        '''
        Method that sends HEAD request to server to ask if file exists.
        :param index: File to be queried
        :return: 0 if found, 1 if not, 2 if connection error
        '''
        file = self.__skFiles[index]
        try:
            r = requests.head(self.__url + file.path, timeout=self.__timeout)
            val = r.status_code
            if val==200:
                #File exists, okay to request
                return 0
            else:
                #File not found
                return 1

        except requests.RequestException as e:
            #Server is unreachable
            return 2


    def skBuildDir(self, path):
        '''
        Method that retrieves directory file from server and builds the skFiles array,
        First builds the file from bytes, then reads it in lines by text
        '''
        try:
            r = requests.get(self.__url + path, timeout = self.__timeout)
            if(r.headers.get('content-type')=='text/html'):
                return 3
        except Exception as e:
            # print(e)
            return 2 #Can't contact server
        if(r.status_code==200):
            try:
                with open("serverdirectory.txt", "wb") as text_file:
                    text_file.write(r.content)
            except Exception as e:
                # print(e)
                #Issue creating server directory
                return 1
        else:
            return 3 #Can't find file
        try:
            with open("serverdirectory.txt", 'r', encoding='utf-8') as text_file:
                self.__dir = text_file.readlines()
        except Exception as e:
            # print(e)
            return 1
        try:
            self.__dir.pop()
            self.__skFiles = []
            for x in self.__dir:
                skFData = x.split('&%&')
                skf = SKFile(skFData[0], skFData[1], skFData[2], skFData[3], skFData[4], skFData[5])
                self.__skFiles.append(skf)
            return 0
        except IndexError:
            return 3


    def skBatchFile(self, index, folder):
        '''
        Windows doesn't like : in titles, great. Maybe just disable batch files altogether?
        :param index:
        :param folder:
        :return:
        '''
        folder = ''.join(e for e in folder if e.isalnum())
        path = os.path.join('batches',folder.strip())
        path2=os.path.join(os.getcwd(),path)
        print(path2)
        if(not os.path.isdir(path2)):
            os.makedirs(path2)
        file = self.__skFiles[index]
        fPath = file.path.rsplit('/',1)
        val = self.skCheckFile(index)
        if (val == 0):
            try:
                r = requests.get(self.__url + file.path, timeout=self.__timeout)
                with open((os.path.join(path2, fPath[1])), "wb") as musicFile:
                    musicFile.write(r.content)
                    musicFile.flush()
                return 0
                # if (file.title.endswith('.mp3')):
                #     with open((os.path.join(path2, file.title)), "wb") as musicFile:
                #         musicFile.write(r.content)
                #         musicFile.flush()
                #         musicFile.close()
                # else:
                #     filetitle2 = file.title + '.mp3'
                #     print(filetitle2)
                #     print(os.path.join(path2, filetitle2))
                #     data = r.content
                #     with open((os.path.join(path2, filetitle2)), "wb") as musicFile:
                #         musicFile.write(data)
                #         musicFile.flush()
                # return 0
            except Exception as e:
                print(e)
                return 1


    def skTestSend(self):
        r = requests.get(self.__url + 'directory.txt', auth=HTTPBasicAuth('James','followme') ,timeout=self.__timeout)
        # print(r.text)

    def skUserComm(self, command):
        '''
        Method for testing things without using GUI
        '''

        if (command == 'update'):
            val = self.skBuildDir()
            if(val == 0):
                return  0
            else:
                return 1
        elif (command == 'exit'):
            self.skCleanUp()
            sys.exit()  # REMOVE LATER

if __name__ == "__main__":
    ClientK = SKHTTPClient(65535, '184.75.148.148', 1, 0.5)
    val = ClientK.skTestConnection()
    # print(val)
    ClientK.skBuildDir('E:\Code2\PyCharm\Projects\SK1.3\\venv\directory.txt')
    val = ClientK.skBatchFile(1,' folder: ')
    val = ClientK.skBatchFile(2,'folder')
    print(val)
    # ClientK.skBuildDir("E:/Code2/PyCharm/Projects/SK1.2/venv/directory.txt")
    # ClientK.skCheckFile(10)
        # command = raw_input("Enter Command")
#         ClientK.connecter()
#         ClientK.trueSend("'Pridemoor Keep' Shovel Knight Remix-k3IKgJUTjlM.mp3".encode())
#         ClientK.commSwitch2("'Pridemoor Keep' Shovel Knight Remix-k3IKgJUTjlM.mp3")
#         print('done')
#         break
