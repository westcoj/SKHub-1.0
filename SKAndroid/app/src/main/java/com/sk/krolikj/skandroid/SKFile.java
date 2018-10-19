package com.sk.krolikj.skandroid;

public class SKFile {

    private String filePath;
    private int songIndex;
    private String songTitle;
    private String songArtist;
    private String songAlbum;

    public SKFile(String path, int index, String title, String artist, String album){
        filePath = path;
        if(title != null)
            songTitle = title;
        else
            songTitle = path;
        if(artist != null)
            songArtist = artist;
        else
            songArtist = "";
        if(album != null)
            songAlbum = album;
        else
            songAlbum = "";
        songIndex = index;
    }

    public String toString(){
        return filePath + " &%& " + songIndex + " &%& " + songTitle +
                " &%& " + songArtist + " &%& " + songAlbum;
    }

}
