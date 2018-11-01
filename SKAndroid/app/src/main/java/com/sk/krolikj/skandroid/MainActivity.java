package com.sk.krolikj.skandroid;

import android.media.MediaPlayer;
import android.media.session.MediaController;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;

import java.io.DataInputStream;
import java.io.DataOutput;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.net.Socket;
import java.net.UnknownHostException;
import java.nio.ByteBuffer;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private int portNum;
    private String dirPath;
    private String hostName;
    private boolean sockStatus;
    private Socket sock;
    private DataInputStream dIS;
    private DataOutputStream dOS;
    private ArrayList directory;
    private ArrayList <SKFile> skFile;
    private MediaPlayer mp;
    private MediaController mc;


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

    public void setDirectory(String path){
        dirPath = path;
    }

    public ArrayList getDirectory(){
        return skFile;
    }

    public void skSetIpHost(String host, int port){
        hostName = host;
        portNum = port;
        Log.d("IP/HOST", hostName + "/" + portNum);
    }

    private int skOpen(){
        try{
            sock = new Socket(hostName, portNum);
            dIS = new DataInputStream(sock.getInputStream());
            dOS = new DataOutputStream(sock.getOutputStream());
            sockStatus = true;
            Log.d("OPEN", "Connection Established");
            return 0;
        }catch(IOException e){
            Log.e("!OPEN", e.toString());
            return 1;
        }
    }

    private void skClose() throws IOException {
        sock.close();
        sockStatus = false;
    }

    private void skSend(String s){
        int len;
        byte[] sendB;
        ByteBuffer buff;
        try {
            dOS = new DataOutputStream(sock.getOutputStream());
            len = s.getBytes().length;
            buff = ByteBuffer.allocate(len+4);
            buff.putInt(len);
            buff.put(s.getBytes());
            sendB = buff.array();
            dOS.write(sendB);
            dOS.flush();
            Log.d("SENT", "Data Sent");
        }catch (IOException e){
            Log.e("!SEND", e.toString());
        }
    }

    public byte[] skRecieve(){
        byte[] rawSize = skRcvAll(4);
        ByteBuffer bBuf = ByteBuffer.wrap(rawSize);
        int size = bBuf.getInt();
        return skRcvAll(size);
    }

    public byte[] skRcvAll(int length){
        byte[] buffer = new byte[length];
        try {
            //DataInputStream is = new DataInputStream(sock.getInputStream());
            if(dIS.read(buffer) < buffer.length) {
                dIS.read(buffer);
            }
            //Log.d("RECEIVE", new String(buffer));
            //is.close();
        }catch(IOException e){
            Log.e("RECEIVE", e.toString());
        }
        return buffer;
    }

    public int skRCVFileIndex(int index){
        String name;
        String path;
        byte[] fileData;
        File file;
        if(sockStatus == false){
            skOpen();
        }
        skSend(Integer.toString(index));
        fileData = skRecieve();
        try{
            name = skFile.get(index).getFilePath();
        }catch(Exception e) {
            return 0;
        }
        if(fileData.length == 0){


        }
        return 0;


    }

    public void audioPlayer(String path, String fileName){
        try {
            mp = new MediaPlayer();
            mp.setDataSource(path + "/" + fileName);
            mp.prepare();
            mp.start();
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mp = MediaPlayer.create(this, R.raw.music);
        mp.setLooping(true);
        mp.seekTo(0);
        mp.setVolume(0.5f, 0.5f);
    }

    private class ConnectTask extends AsyncTask<Void, Void, Void>{

        @Override
        protected Void doInBackground(Void... params){
            byte[] fileData;
            skSetIpHost("192.168.1.78", 9222);
            skOpen();
            if(sockStatus) {
                skSend("ls");
                Log.d("RECEIVE", new String(skRecieve()));
//                try {
//                    skClose();
//                    Log.d("CLOSE", "Connection Closed");
//                } catch (IOException e) {
//                    Log.e("CLOSE", e.toString());
//                }
            }
            return null;
        }
    }

    public void connect(View view){
        new ConnectTask().execute();
    }
//        skSetIpHost(findViewById(R.id.ipBox).toString(),
//                Integer.parseInt(findViewById(R.id.portBox).toString()));
//    }
    public void playPause(View view){
        if(mp.isPlaying()) {
            mp.pause();
        } else {
            mp.start();
        }
    }

    public void skipSong(View view){

    }
}