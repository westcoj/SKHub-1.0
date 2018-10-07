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
        Constructor for test
        '''
        
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
        
    def skToString(self):
        '''
        Method for sending File info as single string
        '''
        
        return self.path + "&%&" + str(self.index) + '&%&' + self.title +"&%&" + self.artist + "&%&" + self.album
    
    def __repr__(self):
        '''
        Method for displaying file name as string
        '''
        return self.path + " &%& " + str(self.index) + ' &%& ' + self.title +" &%& " + self.artist + " &%& " + self.album
