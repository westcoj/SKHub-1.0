'''
Created on Sep 7, 2018
 @author: C
'''
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from socket import gethostname, gethostbyname
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from pip._vendor.distlib.compat import raw_input
from SKFile import SKFile
import configparser
import threading
from urllib.parse import unquote

root = 'hi'
class SKHTTPServer(object):
    def __init__(self):
        '''
        Constructor sets up the server and the raw_input handler. Server is split into two threads,
        one allowing for console input, and another for taking in HTTP requests. Important to
        have all items that will be sent to client in file form, for if user wants to use already
        set up server. In addition admin options will be optional since there's a lack of security.
        homeDir: Grabs the working directory for future use (os.chdir is used in directory walk, meaning we need a way to return)
        port: the port the server will operate on
        path: default directory
        skFiles: List of all songs in SKFile format.
        dir: list of all songs in string format (For sending to client, probably not needed since skfiles have
         this capability)
        '''
        self.__homeDir = os.getcwd()
        self.__hostname = gethostbyname(gethostname())
        self.__pubStats = [0, 0, 0]  # Files Had, Files Served, Unique Conns Made
        self.__ipList = []
        self.__killServer = False
        self.skSetup()
        root = self.__path
        self.__SSAddress = (self.__hostname, self.__port)
        print("hostname: {0}\nport: {1}".format(self.__hostname, self.__port))
        print("__SSAddress: {0}".format(self.__SSAddress))
        def handler(*args):
            return SKHTTPServerHandler(self.__homeDir, self.__pubStats, *args)
        self.__homeDir = self.__homeDir + '/'
        print("os cwd: {0}\n".format(self.__homeDir))
        self.__SS = HTTPServer(self.__SSAddress, handler)
        print("Stopping point.")
        self.__skFiles = []
        self.__dir = self.skBuildDir(self.__path);
        self.__reset = 0
        self.__exitVal = 0

    def skReset(self):
        return self.__reset

    def skSetup(self):
        '''
        Method for reading the ini file provided to the server
        UPDATE: PATH CHECKING
        '''
        # Ensure path is correct
        os.chdir(self.__homeDir)
        if (os.path.isfile('settings.ini')):
            # Process ini file
            try:
                config = configparser.ConfigParser()
                config.read('settings.ini')
                self.__port = int(config['DEFAULT']['ServerPort'])
                # self.__pass = config['DEFAULT']['ConnectionPassword']
                # self.__admPass = config['DEFAULT']['AdminPassword']
                self.__path = config['DEFAULT']['ServerDirectory']
                self.__pubStats[1] = int(config['STATS']['FilesServed'])
                self.__pubStats[2] = int(config['STATS']['ConnectionsMade'])
                try:
                    self.__ipList = config['IPADDRS']['LIST'].split(',')
                except:
                    pass
            except Exception as e:
                print(e)
                if (os.path.isfile('settings.ini.bak')):
                    os.remove('settings.ini.bak')
                print('Issue reading ini file')
                os.rename('settings.ini', 'settings.ini.bak', src_dir_fd=None, dst_dir_fd=None)
                self.skSetup()
        else:
            try:
                config = configparser.ConfigParser()
                self.__port = int(raw_input("Enter server port (default 80):  "))
                # self.__pass = raw_input("Enter connection password:  ")
                # self.__admPass = raw_input("Enter admin control password:  ")
                self.__path = raw_input("Enter absolute file directory path:  ")
                if (not self.__path.endswith('\\')):
                    self.__path += '\\'
                # JAMIE'S USE ONLY:
                self.__path = '/Users/jamiepenzien/Desktop/SKHub-1.0/Music/'
                print("path: " + self.__path)
                config['DEFAULT'] = {}
                config['DEFAULT']['ServerPort'] = str(self.__port)
                # config['DEFAULT']['ConnectionPassword'] = self.__pass
                # config['DEFAULT']['AdminPassword'] = self.__admPass
                config['DEFAULT']['ServerDirectory'] = self.__path
                config['STATS'] = {}
                config['STATS']['FilesServed'] = str(self.__pubStats[1])
                config['STATS']['ConnectionsMade'] = str(self.__pubStats[2])
                config['IPADDRS'] = {}
                ipstring = ''
                for x in self.__ipList:
                    print(x)
                    ipstring = ipstring + (str(x) + ',')
                config['IPADDRS']['LIST'] = ipstring
                with open('settings.ini', 'w') as iniFile:
                    config.write(iniFile)
            except Exception as e:
                print(e)
                print('Error making ini file')
    def skUpdateINI(self):
        # print(self.__ipList)
        os.chdir(self.__homeDir)
        try:
            #             if(os.path.isfile('settings.ini')):
            #                 os.remove('settings.ini')
            config = configparser.ConfigParser()
            config['DEFAULT'] = {}
            config['DEFAULT']['ServerPort'] = str(self.__port)
            # config['DEFAULT']['ConnectionPassword'] = self.__pass
            # config['DEFAULT']['AdminPassword'] = self.__admPass
            config['DEFAULT']['ServerDirectory'] = self.__path
            config['STATS'] = {}
            config['STATS']['FilesServed'] = str(self.__pubStats[1])
            config['STATS']['ConnectionsMade'] = str(self.__pubStats[2])
            config['IPADDRS'] = {}
            ipstring = ''
            for x in self.__ipList:
                ipstring = ipstring + (str(x) + ',')
            config['IPADDRS']['LIST'] = ipstring
            with open('settings.ini', 'w') as iniFile2:
                config.write(iniFile2)
        except Exception as e:
            print(e)
            print('Error making ini file')

    def skRunApp(self):
        self.__serverThread = threading.Thread(target=self.skRunServer, args=())
        self.__serverThread.start()
        self.skRunConsole()

    def skRunServer(self):
        '''
        This method starts up the SKHTTPServerHandler in a new thread
        '''
        print('Now running HTTP server\n')
        self.__SS.serve_forever()

    def skRunConsole(self):
        '''
        This method runs the console of the server for further input. Also handles resets/shutdown.
        '''
        helpMessage = ('Use the console to pass in commands to app & server. \n'
              'EXIT: Close down the server, save files and exit the app\n'
              'RESET: Close down server, save files, and reboot it\n'
              'STATS: Print out various stats about the server\n'
              'HELP: Display this message again\n'
              )
        print(helpMessage)
        exit = 0
        while(exit == 0):
            command = raw_input('Enter Command: ')
            if(command.upper()=='EXIT'):
                exit = 1;
                self.__SS.shutdown()
                self.__SS.server_close()
                self.__serverThread.join(5)
                self.skUpdateINI()
                print('Closing down app')
            elif(command.upper()=='RESET'):
                exit = 1;
                self.__SS.shutdown()
                self.__SS.server_close()
                self.__serverThread.join(5)
                self.skUpdateINI()
                self.__reset = 1
                print('Resetting app')
            elif(command.upper()=='HELP'):
                print(helpMessage)
            elif(command.upper()=='STATS'):
                print('Total # of music files: ' + str(self.__pubStats[0]))
                print('Total # of music files served: ' + str(self.__pubStats[1]))
                print('List of unique IP connections (' + str(self.__pubStats[2]) +'): ')
                for x in self.__ipList:
                    print(x)
            else:
                print('Not a valid command')

    def skBuildDir(self, path):
        '''
        Method that sets the directory for the server to use. Future iterations should support
        multiple directories. This method is OS based and is assuming the user is on Windows
        path: The location of the directory to be used.
        '''
        retArr2 = ""
        self.__skFiles = []
        self.__errList = []

        i = 0
        print("Arrived within BuildDir")
        for root, dirs, files in os.walk(path):
            for name in files:
                # if(root == '.'):
                # sys.stdout.buffer.write((name+'\n').encode()  )
                if (name.endswith('.mp3')):
                    try:
                        # sys.stdout.buffer.write((name+'\n').encode())
                        path  = os.path.join(root,name)
                        tag = MP3(path, ID3=EasyID3)
                        if 'title' in tag:
                            title = tag['title'][0]
                        else:
                            title = name
                        if 'artist' in tag:
                            artist = tag['artist'][0]
                        else:
                            artist = ''
                        if 'album' in tag:
                            album = tag['album'][0]
                        else:
                            album = ''
                        time = tag.info.length
                        skF = SKFile(path, i, title, artist, album, time)
                        i += 1
                        self.__skFiles.append(skF)
                        self.__pubStats[0] += 1
                    # Special duration error on TinyTag Most likely Throws 2 errors
                    except Exception as e:
                        print(e)
                        self.__errList.append(name)
                        pass

        for x in self.__skFiles:
            retArr2 = retArr2 + x.skToString() + '\n'
        #             sys.stdout.buffer.write((x.skToString()+'\n').encode())
        #         for x in self.__errList:
        #             sys.stdout.buffer.write((x+'\n').encode())
        self.skBuildDirFile()
        return retArr2

    def skBuildDirFile(self):
        '''This builds a file based off skFiles for sending to client'''
        try:
            with open("directory.txt", "w") as text_file:
                for x in self.__skFiles:
                    text_file.write(x.skToString() + '\n')
            return 0
        except Exception:
            print('Problem building directory text')
            return 1

class SKHTTPServerHandler(BaseHTTPRequestHandler):
    def __init__(self, root, pubStats, *args):
        self.__root = root
        try:
            BaseHTTPRequestHandler.__init__(self, *args)
        except ConnectionResetError:
            return

    def do_HEAD(self):
        print(self.path)
        self.path = unquote(self.path)
        self.path = self.path[1:]
        self.path = self.path.strip()
        if self.path.endswith('mp3'):
            '''Send out a media file for playing/downloading'''
            check = os.path.isfile(self.path)
            if check:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                return
            else:
                self.send_error(404, 'File not found')

    def do_GET(self):
        '''
        The equivalent of skclientcomm, allowing clients to get the items they need.
        Sends out mp3 files, the stat file, or the directory file
        '''
        self.path = unquote(self.path)
        self.path = self.path[1:]
        self.path = self.path.strip()
        print("path: " + self.path)
        print(self.headers)

        try:
            if self.path.endswith('mp3'):
                '''Send out a media file for playing/downloading'''
                file = open(self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type','data/bytes')
                self.end_headers()
                self.wfile.write(file.read())
                file.close()
                return
            elif(self.path.endswith('directory.txt')):
                '''Send out the directory file'''
                print('Sending Directory')
                file = open(self.__root + 'directory.txt', 'rb')
                print("\nDirectory: " + self.__root + '/directory.txt')
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(file.read())
                file.close()
                return
            elif (self.path.endswith('stats.txt')):
                '''Send out current stats file'''

        except IOError:
            try:
                self.send_error(404,'file not found')
            except ConnectionResetError or ConnectionAbortedError:
                '''Client swapped before message could be sent'''
                pass

        except ConnectionAbortedError:
            '''Client swapped before message could be sent'''
            pass

    def do_POST(self):
        '''Client is changing the server settings'''

    def do_PUT(self):
        '''Client has tagging enabled an has changed file tags'''
     #
    # def log_message(self, format, *args):
    #     '''Override to stop printing to console'''
    #     return
if __name__ == "__main__":
    val = 1
    while(val==1):
        skHTTP = SKHTTPServer()
        skHTTP.skRunApp()
        val = skHTTP.skReset()
    os._exit(0)
