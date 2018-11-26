package com.sk.krolikj.skandroid;


import android.content.Context;
import android.content.Intent;
import android.media.MediaPlayer;
import android.media.session.MediaController;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;

import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.DataOutput;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.net.Socket;
import java.net.URL;
import java.net.UnknownHostException;
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.LinkOption;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private URL theUrl;
    private String theHostName;
    private String thePortNum;
    private File song;
    private TextView mTextMessage;
    private int portNum;
    private String dirPath;
    private String hostName;
    private boolean sockStatus;
    private Socket sock;
    private DataInputStream dIS;
    private DataOutputStream dOS;
    private String[] directory;
    private ArrayList <SKFile> skFile;
    private ArrayList <SKFile> lib;
    private MediaPlayer mp;
    private MediaController mc;
    private File cacheDir;
    private File ouputFile;
    private Context appContext;
    private ArrayList<SKFile> cache;
    private final static int CACHEMAX = 5;
    private BottomNavigationView navigation;
    private HomeFragment homeFragment;
    private PlayerFragment playerFragment;
    private ConfigFragment configFragment;



//    public MainActivity(String path, int port, String ip){
//        dirPath = path;
//        portNum = port;
//        hostName = ip;
//        sockStatus = false;
//        directory = new ArrayList<String>();
//        skFile = new ArrayList<String>();
//        mp = new MediaPlayer();
//        mc = new MediaController();
//    }

//    public int skSetup(MainActivity act){
//        /*Old method might not need*/
//        return 0;
//    }
//
//    public void skWriteSKC(){
//        /*Old method might not need*/
//    }

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

    public ArrayList<SKFile> getFullLibrary(){
        return lib;
    }
    public void setFullLibrary(ArrayList<SKFile> list){
        lib = list;
    }

    public void setSong(File filepath){
        song = filepath;
    }

    public File getSong(){
        return song;
    }

    public void skSetIpHost(String host, int port){
        theHostName = host;
        thePortNum = Integer.toString(port);
        //Log.d("IP/HOST", hostName + "/" + portNum);
    }

//
//    private int skOpen(){
////        try{
////            sock = new Socket(hostName, portNum);
////            dIS = new DataInputStream(sock.getInputStream());
////            dOS = new DataOutputStream(sock.getOutputStream());
////            sockStatus = true;
////            Log.d("OPEN", "Connection Established");
////            return 0;
////        }catch(IOException e){
////            Log.e("!OPEN", e.toString());
////            return 1;
////        }
////    }
    public String getHostPort(){
        return theHostName + "/" + thePortNum;
    }

    public void setURL(URL url){
        theUrl = url;
    }

    public URL getURL(){
        return theUrl;
    }

//    private void skClose() throws IOException {
//        sock.close();
//        sockStatus = false;
//    }

//    private boolean skCacheCheck(int index){
//        return cache.contains(cache.get(index));
//    }

//    private void skSend(String s){
//        int len;
//        byte[] sendB;
//        ByteBuffer buff;
//        try {
//            dOS = new DataOutputStream(sock.getOutputStream());
//            len = s.getBytes().length;
//            buff = ByteBuffer.allocate(len+4);
//            buff.putInt(len);
//            buff.put(s.getBytes());
//            sendB = buff.array();
//            dOS.write(sendB);
//            dOS.flush();
//            Log.d("SENT", "Data Sent");
//        }catch (IOException e){
//            Log.e("!SEND", e.toString());
//        }
//    }

//    public byte[] skRecieve(){
//        byte[] rawSize = skRcvAll(4);
//        ByteBuffer bBuf = ByteBuffer.wrap(rawSize);
//        int size = bBuf.getInt();
//        return skRcvAll(size);
//    }
//
//    public byte[] skRcvAll(int length){
//        byte[] buffer = new byte[length];
//        try {
//            //DataInputStream is = new DataInputStream(sock.getInputStream());
//            if(dIS.read(buffer) < buffer.length) {
//                dIS.read(buffer);
//            }
//            //Log.d("RECEIVE", new String(buffer));
//            //is.close();
//        }catch(IOException e){
//            Log.e("RECEIVE", e.toString());
//        }
//        return buffer;
//    }
//
//    public int skUIFile(int index)throws IOException{
//        int con;
//        byte[] ansData;
//        String ans;
//        SKFile temp;

//        if(skCacheCheck(index)){
//            temp = cache.get(index);
//            cache.remove(index);
//            cache.add(temp);
//            return 0;
//        }
//        con = skOpen();
//        if(con == 0){
//            skSend("file");
//            ansData = skRecieve();
//            if(ansData != null){
//                ans = new String(ansData);
//                if(ans.equals("okay")){
//                    return skRCVFileIndex(index);
//                }else{
//                    return -5;
//                }
//            }else{
//                return -5;
//            }
//            //skClose();
//        }
//        return -5;
//    }
//
//    public int skRCVFileIndex(int index) throws IOException{
//        String name = "";
//        String path = "";
//        byte[] fileData;
//        SKFile file;
//        //Path p;
//
//        if(!sockStatus){
//            skOpen();
//        }
//        skSend(Integer.toString(index));
//        fileData = skRecieve();
//        try{
//            name = skFile.get(index).getsongIndex() + ".mp3";
//        }catch(Exception e) {
//            Log.e("NAMING", e.toString());
//        }
//        Log.d("FILE DATA", fileData.length + "");
//        if(fileData.length != 0){
//            path = dirPath + "\\" + name;
//            p = Paths.get(dirPath + name);
//            if(Files.notExists(p)){
//                new File(path).mkdirs();
//            }
//            FileOutputStream fos = new FileOutputStream(path);
//            fos.write(fileData);
//            fos.close();
//            skFile.get(index).skAddPath(path);
//            if(cache.size() > CACHEMAX){
//                file = cache.remove(0);
//                appContext.deleteFile(file.getCachePath());
//            }
//            cache.add(skFile.get(index));
//            skClose();
//            return 0;
//        }else {
//            skClose();
//            return 1;
//        }
//    }

//    public int userComm(String command) throws IOException{
//        int val;
//        byte[] data;
//        String[] skData;
//        String dataString;
//        SKFile sk;
//        if(command.equals("update")){
//            val = skOpen();
//            if(val == 1) {
//                Log.e("OPEN", "Error connecting to server");
//                return 1;
//            }
//            skSend("ls");
//            data = skRecieve();
//            dataString = new String(data);
//            System.out.println(dataString);
//            directory = dataString.split("\n");
//            for(String x: directory){
//                skData = x.split("&%&");
//                System.out.println(x);
//                if(skData.length == 5) {
//                    sk = new SKFile(skData[0], Integer.parseInt(skData[1]),
//                            skData[2], skData[3], skData[4]);
//                    skFile.add(sk);
//                }
//            }
//            skClose();
//        }else if(command == "ls"){
//            int i = 0;
//            while (i < directory.length){
//                System.out.println(i + ": " + directory[i]);
//                i++;
//            }
//        }else if(command == "file"){
//            val = skOpen();
//            if(val == 1) {
//                Log.e("OPEN", "Error Contacting Server");
//                return 1;
//            }
//        }
//        return 0;
//    }

    public void skCleanUp(){
        for(SKFile x: cache){
            appContext.deleteFile(x.getCachePath());
        }
    }

//    public void audioPlayer(String path, String fileName){
//        try {
//            mp = new MediaPlayer();
//            mp.setDataSource(path + "/" + fileName);
//            mp.prepare();
//            mp.start();
//        }catch(Exception e){
//            e.printStackTrace();
//        }
//    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        navigation = findViewById(R.id.navigation);
        homeFragment = new HomeFragment();
        playerFragment = new PlayerFragment();
        configFragment = new ConfigFragment();
        cache = new ArrayList<SKFile>();


        navigation.setOnNavigationItemSelectedListener(new BottomNavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
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

    //    };

        appContext = getApplication();
        //cacheDir = getCacheDir();
        //dirPath = cacheDir.toString();
        skFile = new ArrayList<SKFile>();
        cache = new ArrayList<SKFile>();

//        mp = MediaPlayer.create(this, R.raw.music);
//        mp.setLooping(true);
//        mp.seekTo(0);
//        mp.setVolume(0.5f, 0.5f);

        mTextMessage = (TextView) findViewById(R.id.message);
        //navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);
    }

//    private class ConnectTask extends AsyncTask<Void, Void, Void>{
//
//        @Override
//        protected Void doInBackground(Void... params){
//            byte[] fileData;
//            skSetIpHost("192.168.1.78", 9222);
//            //skOpen();
//            System.out.println(dirPath);
//            try {
//                userComm("update");
//                skUIFile(0);
//            } catch (IOException e) {
//                Log.e("UIFILE", e.toString());
//            }
//            return null;
//        }
//    }

    public void setFragment(Fragment frag){
        FragmentTransaction fragTrans = getSupportFragmentManager().beginTransaction();
        fragTrans.replace(R.id.mainFrame, frag);
        fragTrans.commit();
    }

//    public void connect(View view){
//        new ConnectTask().execute();
//    }

//    public void playPause(View view){
//        if(mp.isPlaying()) {
//            mp.pause();
//        } else {
//            mp.start();
//        }
//    }
//
//    public void skipSong(View view){
//
//    }
}

