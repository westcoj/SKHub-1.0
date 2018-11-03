'''
Created on Sep 25, 2018

@author: Cody
'''

class SKFile(object):
    '''
    Class that contains metadata and index number of song
    '''


    def __init__(self, path, index, title, artist, album):
        '''
        Constructor gets called by directory lookups and song distribution, this makes it easier to
        keep track of song files, without actually holding onto the files.. Any relevant info
        is placed in the proper variable, if that info isn't present a blank is assigned instead.
        '''
        
        #Path is used by the server when servicing requests by the client.
        self.path = path
        if title:
            self.title = title
        else:
            self.title = path
        if artist:
            self.artist = artist
        else:
            self.artist = ''
        if album:
            self.album = album
        else:
            self.album = ''
        self.index = index
        self.cachePath = ''
        
    def skToString(self):
        '''
        This method prints the file information in one string.
        '''
        
        return self.path + "&%&" + str(self.index) + '&%&' + self.title +"&%&" + self.artist + "&%&" + self.album
    
    def __repr__(self):
        '''
        This method is the same above, but is the python overwrite in calling print()
        '''
        return self.path + " &%& " + str(self.index) + ' &%& ' + self.title +" &%& " + self.artist + " &%& " + self.album
    
    def skAddPath(self, path):
        '''Method that adds a cache path to skFile for cache use'''
        self.cachePath = path
