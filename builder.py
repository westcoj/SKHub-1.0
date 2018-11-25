'''
Created on Sep 7, 2018
@author: C
'''
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from pip._vendor.distlib.compat import raw_input
import time
import sys


class SKFile(object):
    '''
    Class that contains metadata of song
    '''

    def __init__(self, url, name, artist, album):
        '''
        Constructor gets called by directory lookups and song distribution, this makes it easier to
        keep track of song files, without actually holding onto the files.. Any relevant info
        is placed in the proper variable, if that info isn't present a blank is assigned instead.
        '''

        # url is used by the server when servicing requests by the client.
        url = url.replace("\\", "/")
        self.url = url
        if name:
            self.name = name
        else:
            self.name = url
        if artist:
            self.artist = artist
        else:
            self.artist = ''
        if album:
            self.album = album
        else:
            self.album = ''
        # if time:
        #     self.time = float(time)
        # else:
        #     self.time = 0
        # self.index = index

    def skToString(self):
        '''
        This method prints the file information in one string.
        '''

        return self.url + " &%& " + str(
            self.index) + ' &%& ' + self.name + " &%& " + self.artist + " &%& " + self.album + "&%&" + str(self.time)

    def __repr__(self):
        '''
        This method is the same above, but is the python overwrite in calling print()
        '''
        return (
                'url: ' + self.url + "\n" +
                # 'index: ' + str(self.index) + '\n' +
                'name: ' + self.name + "\n" +
                'artist: ' + self.artist + "\n" +
                'album: ' + self.album + '\n' )
                # 'time: ' + self.time)

if __name__ == "__main__":
    retArr2 = []
    path = os.getcwd()
    i = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            # if(root == '.'):
            # sys.stdout.buffer.write((name+'\n').encode()  )
            if (name.endswith('.mp3')):
                try:
                    # sys.stdout.buffer.write((name+'\n').encode())
                    path2 = os.path.join(root, name)
                    tag = MP3(path2, ID3=EasyID3)
                    if 'name' in tag:
                        name = tag['name'][0]
                    else:
                        name = name
                    if 'artist' in tag:
                        artist = tag['artist'][0]
                    else:
                        artist = ''
                    if 'album' in tag:
                        album = tag['album'][0]
                    else:
                        album = ''
                    time = tag.info.length
                    if(root=='.'):
                        url = root.replace(path, '.') + name
                    else:
                        url = root.replace(path, '.') + '\\' + name

                    skFile = SKFile(url, name, artist, album)
                    retArr2.append(skFile)
                    i += 1
                # Special duration error on TinyTag Most likely Throws 2 errors
                except Exception as e:
                    print(e)
                    pass

    # print(retArr2)
    print("\"songs\": [" )
    i=0
    for x in retArr2:
        print("{")
        sys.stdout.buffer.write(("\"name\": " + '\"' + x.name + '\",' + '\n').encode())
        sys.stdout.buffer.write(("\"artist\": " + '\"' + x.artist + '\",' +'\n').encode())
        sys.stdout.buffer.write(("\"album\": " + '\"' + x.album + '\",' + '\n').encode())
        sys.stdout.buffer.write(("\"url\": " + '\"' + x.url + '\",' + '\n').encode())
        sys.stdout.buffer.write(("\"keydex\": " + '\"' + str(i) + '\"' + '\n').encode())
        print("},")
        i+=1;
    print(']')

    exit = raw_input("Hit enter when ready: ")


    # for x in self.__skFiles:
    #     retArr2 = retArr2 + x.skToString() + '\n'
    #             sys.stdout.buffer.write((x.skToString()+'\n').encode())
    #         for x in self.__errList:
    #             sys.stdout.buffer.write((x+'\n').encode())