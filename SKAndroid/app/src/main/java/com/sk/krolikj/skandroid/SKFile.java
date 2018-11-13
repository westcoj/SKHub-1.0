package com.sk.krolikj.skandroid;

public class SKFile {

    private String filePath;
    private int songIndex;
    private String songTitle;
    private String songArtist;
    private String songAlbum;
    private String cachePath;

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

    public String getFilePath(){
        return filePath;
    }

    public int getsongIndex(){
        return songIndex;
    }

    public String getSongTitle(){
        return songTitle;
    }

    public String getSongArtist(){
        return songArtist;
    }

    public String getSongAlbum(){
        return songAlbum;
    }

    public String getCachePath() {
        return cachePath;
    }

    public void skAddPath(String path){
        cachePath = path;
    }

    public String toString(){
        return filePath + " &%& " + songIndex + " &%& " + songTitle +
                " &%& " + songArtist + " &%& " + songAlbum;
    }

}
