package com.sk.krolikj.skandroid;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.os.PersistableBundle;
import android.support.design.widget.BottomNavigationView;
import android.support.design.widget.TextInputEditText;
import android.support.design.widget.TextInputLayout;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Toast;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;

public class ConfigActivity extends AppCompatActivity {

    private int portNum;
    private String ip;
    private Socket sock;
    private DataInputStream dIS;
    private DataOutputStream dOS;
    private Boolean connectSuccess = false;
    private TextInputLayout ipInput;
    private TextInputLayout portInput;


    public int getPortNum(){
        return portNum;
    }

    public String getIp(){
        return ip;
    }

    public Boolean getConnectSuccess() {
        return connectSuccess;
    }

    public void skSetIpHost(String host, int port){
        ip = host;
        portNum = port;
        Log.d("IP/HOST", ip + "/" + portNum);
    }

    private int skOpen(){
        try{
            sock = new Socket();
            sock.connect(new InetSocketAddress(ip, portNum),5000);
            dIS = new DataInputStream(sock.getInputStream());
            dOS = new DataOutputStream(sock.getOutputStream());
            Log.d("OPEN", "Connection Established");
            return 0;
        }catch(IOException e){
            Log.e("!OPEN", e.toString());
            return 1;
        }
    }

    private void skClose() throws IOException {
        sock.close();
    }

//    public void connect(View view){
//        new ConnectTask().execute();
//        Context context = getApplicationContext();
//        if(connectSuccess){
//            Toast toast = Toast.makeText(context, "Server Found", Toast.LENGTH_SHORT);
//            toast.show();
//        }else{
//            Toast toast = Toast.makeText(context, "Could Not Find Server", Toast.LENGTH_SHORT);
//            toast.show();
//        }
//    }

    private class ConnectTask extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... params){
            ipInput = findViewById(R.id.ipInputBox);
            portInput = findViewById(R.id.portInputBox);
            String ipNum = ipInput.getEditText().getText().toString();
            String port = portInput.getEditText().getText().toString();
            ip = ipNum;
            portNum = Integer.parseInt(port);
            skSetIpHost(ip, portNum);
            if(skOpen() == 0){
                connectSuccess = true;
                try {
                    skClose();
                }catch(IOException e){
                    e.printStackTrace();
                }
                return null;
            }else{
                connectSuccess = false;

                return null;
            }
        }
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState){//, @androidx.annotation.Nullable PersistableBundle persistentState) {
        super.onCreate(savedInstanceState);//, persistentState);
        setContentView(R.layout.config_activity);

        BottomNavigationView navigation = (BottomNavigationView) findViewById(R.id.navigation);
        Menu menu = navigation.getMenu();
        MenuItem menuItem = menu.getItem(2);
        menuItem.setChecked(true);

        BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
                = new BottomNavigationView.OnNavigationItemSelectedListener() {

            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                switch (item.getItemId()) {
                    case R.id.navigation_library:
                        Intent intent = new Intent(ConfigActivity.this, MainActivity.class);
                        startActivity(intent);
                        return true;
                    case R.id.navigation_player:
                        Intent intent1 = new Intent(ConfigActivity.this, PlayerActivity.class);
                        startActivity(intent1);
                        return true;
                    case R.id.navigation_config:

                        return true;
                }
                return false;
            }
        };
        navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);
    }
}
