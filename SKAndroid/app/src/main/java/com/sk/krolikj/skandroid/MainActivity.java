package com.sk.krolikj.skandroid;

import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.view.MenuItem;
import android.widget.TextView;

import java.io.DataOutput;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private int portNum;
    private String dirPath;
    private String hostName;
    private boolean sockStatus;
    private Socket sock;
    private ArrayList directory = new ArrayList<String>();
    private ArrayList skFile = new ArrayList<String>();


    public MainActivity(String path, int port, String ip){
        dirPath = path;
        portNum = port;
        hostName = ip;
        sockStatus = false;
    }

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
    }

    private int skOpen(){
        try{
            sock = new Socket(hostName, portNum);
            sockStatus = true;
            return 0;
        }catch(IOException e){
            return 1;
        }
    }

    private void skClose() throws IOException {
        sock.close();
        sockStatus = false;
    }

    private void skSend(String s){
        try {
            DataOutputStream dOS = new DataOutputStream(sock.getOutputStream());
            dOS.writeBytes(s);
            dOS.flush();
        }catch (IOException e){
            System.out.println("Failed to Send");
        }
    }

//    public int skRecieve(){
//
//    }

    private byte[] skRcvAll(int length){
        byte[] buffer = new byte[length];
        FileInputStream is = new FileinputStream(/*FileName*/);

        return buffer;
    }

    private TextView mTextMessage;

    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
            = new BottomNavigationView.OnNavigationItemSelectedListener() {

        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            switch (item.getItemId()) {
                case R.id.navigation_home:
                    mTextMessage.setText(R.string.title_home);
                    return true;
                case R.id.navigation_dashboard:
                    mTextMessage.setText(R.string.title_dashboard);
                    return true;
                case R.id.navigation_notifications:
                    mTextMessage.setText(R.string.title_notifications);
                    return true;
            }
            return false;
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mTextMessage = (TextView) findViewById(R.id.message);
        BottomNavigationView navigation = (BottomNavigationView) findViewById(R.id.navigation);
        navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);
    }

}
