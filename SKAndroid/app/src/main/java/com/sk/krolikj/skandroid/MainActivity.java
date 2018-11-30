package com.sk.krolikj.skandroid;


import android.content.Context;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.design.widget.BottomNavigationView;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.util.SparseArray;
import android.view.MenuItem;
import android.view.ViewGroup;
import android.widget.TextView;

import java.io.File;
import java.lang.ref.WeakReference;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private URL theUrl;
    private String songURL;
    private String theHostName;
    private String thePortNum;
    private SKFile songPlaying;
    private File song;
    private TextView mTextMessage;
    private String dirPath;
    private ArrayList <SKFile> skFile;
    private ArrayList <SKFile> lib;
    private Context appContext;
    private ArrayList<SKFile> cache;
    private final static int CACHEMAX = 5;
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

    public String getSongURL(){
        return songURL;
    }

    public void setSongURL(String url) {
        songURL = url;
    }

    public void skSetIpHost(String host, int port){
        theHostName = host;
        thePortNum = Integer.toString(port);
        //Log.d("IP/HOST", hostName + "/" + portNum);
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

    public boolean getSongSet(){
        return songSet;
    }

    public void setSongSet(boolean status){
        songSet = status;
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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        navigation = findViewById(R.id.navigation);
//        songSet = false;
//        final CustomViewPager viewPager = findViewById(R.id.viewpager1);
//        ViewPagerAdapter adapter = new ViewPagerAdapter (MainActivity.this.getSupportFragmentManager());
//        adapter.addFragment(new HomeFragment(), "title");
//        adapter.addFragment(new PlayerFragment(), "title");
//        adapter.addFragment(new ConfigFragment(), "title");
//        viewPager.setAdapter(adapter);
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
                        //viewPager.setCurrentItem(0);
                        return true;
                    case R.id.navigation_player:
                        setFragment(playerFragment);
                        //viewPager.setCurrentItem(1);
                        return true;
                    case R.id.navigation_config:
                        setFragment(configFragment);
                        //viewPager.setCurrentItem(2);
                        return true;
                }

                return false;
            }
        });

        appContext = getApplication();
        skFile = new ArrayList<SKFile>();
        cache = new ArrayList<SKFile>();

        mTextMessage = (TextView) findViewById(R.id.message);
        //navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);
    }

    private class ViewPagerAdapter extends FragmentPagerAdapter {
        private final SparseArray<WeakReference<Fragment>> instantiatedFragments = new SparseArray<>();
        private final List<Fragment> mFragmentList = new ArrayList<>();
        private final List<String> mFragmentTitleList = new ArrayList<>();

        ViewPagerAdapter(FragmentManager manager) {
            super(manager);
        }

        @Override
        public Fragment getItem(int position) {
            return mFragmentList.get(position);
        }

        @Override
        public int getCount() {
            return mFragmentList.size();
        }

        void addFragment(Fragment fragment, String title) {
            mFragmentList.add(fragment);
            mFragmentTitleList.add(title);
        }

        @Override
        public Object instantiateItem(ViewGroup container, int position) {
            final Fragment fragment = (Fragment) super.instantiateItem(container, position);
            instantiatedFragments.put(position, new WeakReference<>(fragment));
            return fragment;
        }

        @Override
        public void destroyItem(ViewGroup container, int position, Object object) {
            instantiatedFragments.remove(position);
            super.destroyItem(container, position, object);
        }

        @Nullable
        Fragment getFragment(final int position) {
            final WeakReference<Fragment> wr = instantiatedFragments.get(position);
            if (wr != null) {
                return wr.get();
            } else {
                return null;
            }
        }

        @Override
        public CharSequence getPageTitle(int position) {
            return mFragmentTitleList.get(position);
        }
    }

    public void setFragment(Fragment frag){
        FragmentTransaction fragTrans = getSupportFragmentManager().beginTransaction();
        fragTrans.replace(R.id.mainFrame, frag);
        fragTrans.commit();
    }
}

