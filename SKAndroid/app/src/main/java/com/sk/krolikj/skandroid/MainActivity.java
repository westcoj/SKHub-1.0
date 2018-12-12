package com.sk.krolikj.skandroid;


import android.content.Context;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.design.widget.BottomNavigationView;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.view.MenuItem;
import android.widget.TextView;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private URL theUrl;
    private String songURL;
    private String theHostName;
    private String thePortNum;
    private SKFile songPlaying;
    private TextView mTextMessage;
    private String dirPath;
    private ArrayList <SKFile> skFile;
    private ArrayList <SKFile> lib;
    private ArrayList<SKFile> cache;
    private BottomNavigationView navigation;
    private HomeFragment homeFragment;
    private PlayerFragment playerFragment;
    private ConfigFragment configFragment;
    private boolean songSet;


    public void setDirectoryPath(String path){
        dirPath = path;
    }

    public String getDirectoryPath(){
        return dirPath;
    }

    public ArrayList getCache(){
        return cache;
    }

    public void setCache(ArrayList<SKFile> list){
        cache = list;
    }

    public void setSkFile(ArrayList<SKFile> list){
        skFile = list;
    }

    public ArrayList<SKFile> getSkFile(){
        return skFile;
    }

    public void setFullLibrary(ArrayList<SKFile> list){
        lib = list;
    }


    public String getSongURL(){
        return songURL;
    }

    public void setSongURL(String url) {
        songURL = url;
    }

    public void skSetIpHost(String host, int port){
        theHostName = host;
        thePortNum = Integer.toString(port);
    }

    public SKFile getSongData(){
        return songPlaying;
    }

    public void setSongData(SKFile sk){
        songPlaying = sk;
    }

    public String getHostPort(){
        return theHostName + "/" + thePortNum;
    }

    public void setURL(URL url){
        theUrl = url;
    }

    public URL getURL(){
        return theUrl;
    }

    public void setSongSet(boolean status){
        songSet = status;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        try {
            theUrl = new URL("http://184.75.148.148:65535");
        }catch(IOException e){
            e.printStackTrace();
        }
        navigation = findViewById(R.id.navigation);
        homeFragment = new HomeFragment();
        playerFragment = new PlayerFragment();
        configFragment = new ConfigFragment();


        navigation.setOnNavigationItemSelectedListener(new BottomNavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
                switch (item.getItemId()) {
                    case R.id.navigation_library:
                        setFragment(homeFragment);
                        return true;
                    case R.id.navigation_player:
                        setFragment(playerFragment);
                        return true;
                    case R.id.navigation_config:
                        setFragment(configFragment);
                        return true;
                }

                return false;
            }
        });

        skFile = new ArrayList<>();
        cache = new ArrayList<>();

        mTextMessage = (TextView) findViewById(R.id.message);
        //navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);
    }

    public void setFragment(Fragment frag){
        FragmentTransaction fragTrans = getSupportFragmentManager().beginTransaction();
        fragTrans.replace(R.id.mainFrame, frag);
        fragTrans.commit();
    }
}

