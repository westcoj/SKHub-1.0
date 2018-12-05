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
    private CustomViewPager viewPager;
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

    public Fragment getPlayerFragment(){
        return playerFragment;
    }

    public Fragment getHomeFragment(){
        return homeFragment;
    }

    public CustomViewPager getViewPager(){
        return viewPager;
    }

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
//        viewPager = findViewById(R.id.viewpager1);
//        ViewPagerAdapter adapter = new ViewPagerAdapter (MainActivity.this.getSupportFragmentManager());
//        adapter.addFragment(new HomeFragment(), "title");
//        adapter.addFragment(new PlayerFragment(), "title");
//        adapter.addFragment(new ConfigFragment(), "title");
//        viewPager.setAdapter(adapter);
        homeFragment = new HomeFragment();
        playerFragment = new PlayerFragment();
        configFragment = new ConfigFragment();
//        cache = new ArrayList<SKFile>();


        navigation.setOnNavigationItemSelectedListener(new BottomNavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
                switch (item.getItemId()) {
                    case R.id.navigation_library:
//                        ft = getSupportFragmentManager().beginTransaction();
//                        ft.show(homeFragment);
//                        ft.hide(playerFragment);
//                        ft.hide(configFragment);
//                        ft.commit();
                        setFragment(homeFragment);
//                        viewPager.setCurrentItem(0);
                        return true;
                    case R.id.navigation_player:
//                        ft = getSupportFragmentManager().beginTransaction();
//                        ft.show(playerFragment);
//                        ft.hide(homeFragment);
//                        ft.hide(configFragment);
//                        ft.commit();
                        setFragment(playerFragment);
//                        viewPager.setCurrentItem(1);
                        return true;
                    case R.id.navigation_config:
                        setFragment(configFragment);
//                        viewPager.setCurrentItem(2);
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

