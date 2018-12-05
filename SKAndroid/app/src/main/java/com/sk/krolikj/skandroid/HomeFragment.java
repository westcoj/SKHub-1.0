package com.sk.krolikj.skandroid;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.text.InputType;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ListView;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.InetSocketAddress;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.Socket;
import java.net.URL;
import java.net.URLConnection;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Collections;
import java.util.ConcurrentModificationException;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.ExecutionException;


/**
 * A simple {@link Fragment} subclass.
 * Activities that contain this fragment must implement the
 * {@link HomeFragment.OnFragmentInteractionListener} interface
 * to handle interaction events.
 * Use the {@link HomeFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class HomeFragment extends Fragment {
    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;
    private ListView listView;
    private int portNum;
    private String hostName;
    private String dirPath;
    private String playlistName;
    private boolean sockStatus;
    private Socket sock;
    private DataInputStream dIS;
    private DataOutputStream dOS;
    private String[] directory;
    private ArrayList<SKFile> skFile;
    private ArrayList<SKFile> skLibrary;
    private Context appContext;
    private ArrayList<SKFile> cache;
    private final static int CACHEMAX = 5;
    private Button updateButton;
    private Button shuffleButton;
    private Button playlistButton;
    private Button newPlaylistButton;
    private int index;
    private String songPath;
    private SKMedia skm;
    private String songURL;
    File songFile = new File("temp");


    private OnFragmentInteractionListener mListener;

    public HomeFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment HomeFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static HomeFragment newInstance(String param1, String param2) {
        HomeFragment fragment = new HomeFragment();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, final ViewGroup container,
                             Bundle savedInstanceState) {
        final View rootView = inflater.inflate(R.layout.fragment_home, container, false);
        final MainActivity main = (MainActivity)getActivity();

//        if (container != null) {
//            container.removeAllViews();
//        }

        ImageView logo = main.findViewById(R.id.Logo);
        ImageView sounderkin = main.findViewById(R.id.SounderKin);
        logo.setVisibility(View.GONE);
        sounderkin.setVisibility(View.GONE);

        skm = new SKMedia(getContext());
        skm.createDb();

        listView = rootView.findViewById(R.id.my_listview);

        updateButton = rootView.findViewById(R.id.updateButton);
        shuffleButton = rootView.findViewById(R.id.shuffleButton);
        playlistButton = rootView.findViewById(R.id.playlistButton);
        newPlaylistButton = rootView.findViewById(R.id.newPlaylistButton);

        /***************************************
        String config = main.getHostPort();
        String[] str = config.split("/");
        hostName = str[0];
        portNum = Integer.parseInt(str[1]);
         ***************************************/
//        hostName = "192.168.1.97";
//        portNum = 9222;
        skFile = new ArrayList<>();
        skLibrary = new ArrayList<>();

        if(hostName != null) {
            dirPath = main.getDirectoryPath();
            cache = main.getCache();

            try {
                new HomeFragment.UpdateTask().execute().get();
            } catch (InterruptedException | ExecutionException ex) {
                ex.printStackTrace();
            }

            main.setSkFile(skFile);
            ListAdapter adapter = new ListAdapter(getActivity(), skFile);
            listView.setAdapter(adapter);
            listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                    index = skFile.get(position).getSongIndex();
                    main.setSongData(skFile.get(position));
                    main.setSongSet(true);
                    try {
                        new HomeFragment.PlaySong().execute().get();
                    }catch(InterruptedException | ExecutionException ex){
                        ex.printStackTrace();
                    }

                    main.setSong(songFile);
                    System.out.println(main.getSong());
                    final FragmentTransaction ft = getFragmentManager().beginTransaction();
                    ft.replace(R.id.mainFrame, new PlayerFragment());
                    ft.commit();
                }
            });
        }

        View.OnClickListener updateClick = new View.OnClickListener() {
            @Override
            public void onClick(View v){
//                String config = main.getHostPort();
                dirPath = main.getDirectoryPath();
                cache = main.getCache();
//                String[] str = config.split("/");
//                hostName = str[0];
//                portNum = Integer.parseInt(str[1]);
//                skFile = new ArrayList<SKFile>();
                System.out.println(hostName + "/" + portNum);
                try {
                    new HomeFragment.UpdateTask().execute().get();
                }catch(InterruptedException | ExecutionException ex){
                    ex.printStackTrace();
                }

                main.setFullLibrary(skFile);
                main.setSkFile(skFile);
                ListAdapter adapter = new ListAdapter(getActivity(), skFile);
                listView.setAdapter(adapter);

                listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                    @Override
                    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                        index = skFile.get(position).getSongIndex();
                        main.setSongData(skFile.get(position));
                        try {
                            new HomeFragment.PlaySong().execute().get();
                        }catch(InterruptedException | ExecutionException ex){
                            ex.printStackTrace();
                        }

                        main.setSkFile(skFile);
                        main.setSongURL(songURL);
//                        System.out.println(main.getSong());
//                        main.getViewPager().setCurrentItem(1);
                        final FragmentTransaction ft = getFragmentManager().beginTransaction();
                        ft.replace(R.id.mainFrame, new PlayerFragment());
//                        ft.show(main.getPlayerFragment());
//                        ft.hide(main.getHomeFragment());
                        ft.commit();
                    }
                });
            }
        };

        View.OnClickListener shuffleClick = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                skFile = shuffle(skFile);
                main.setSkFile(skFile);
                ListAdapter adapter = new ListAdapter(getActivity(), skFile);
                listView.setAdapter(adapter);
                listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                    @Override
                    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                        index = skFile.get(position).getSongIndex();
                        try {
                            new HomeFragment.PlaySong().execute().get();
                        }catch(InterruptedException | ExecutionException ex){
                            ex.printStackTrace();
                        }
                        for(SKFile x: cache){
                            System.out.println(x.getSongTitle());
                        }
                        main.setSkFile(skFile);
                        main.setSongURL(songURL);
                        System.out.println(main.getSong());
                        final FragmentTransaction ft = getFragmentManager().beginTransaction();
                        ft.replace(R.id.mainFrame, new PlayerFragment());
                        ft.commit();
                    }
                });
            }
        };

        View.OnClickListener playlistClick = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final ArrayList<SKFile> tempList = skm.dbGetAll();
                ListAdapter adapter = new ListAdapter(getActivity(), tempList);
                listView.setAdapter(adapter);
                listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                    @Override
                    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
//                        try {
//                            new HomeFragment.UpdateTask().execute().get();
//                        }catch(InterruptedException | ExecutionException ex){
//                            ex.printStackTrace();
//                        }
//                        while(skFile.size() != 0){
//                            skLibrary.add(skFile.remove(0));
//                        }
                        skFile.clear();
                        skFile = skm.getDataBaseList(tempList.get(position).getFilePath());
                        final ListAdapter songAdapter = new ListAdapter(getActivity(), skFile);
                        listView.setAdapter(songAdapter);
                        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                            @Override
                            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                                index = skFile.get(position).getSongIndex();
                                main.setSongData(skFile.get(position));
                                //File sFile = new File(getActivity().getFilesDir() + "/" + skFile.get(position).getFilePath());
                                try {
                                    new HomeFragment.PlaySong().execute().get();
                                }catch(InterruptedException | ExecutionException ex){
                                    ex.printStackTrace();
                                }

                                main.setSkFile(skFile);
                                main.setSongURL(songURL);
                                //main.setSong(sFile);
                                System.out.println(main.getSong());
                                final FragmentTransaction ft = getFragmentManager().beginTransaction();
                                ft.replace(R.id.mainFrame, new PlayerFragment());
                                ft.commit();
                            }
                        });

                    }
                });
            }
        };

        View.OnClickListener newPlaylistClick = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
                builder.setTitle("Input Playlist Name");
                final EditText input = new EditText(getActivity());
                input.setInputType(InputType.TYPE_CLASS_TEXT);
                builder.setView(input);

                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        playlistName = input.getText().toString();
//                        try {
//                            new HomeFragment.UpdateTask().execute().get();
//                        }catch(InterruptedException | ExecutionException ex){
//                            ex.printStackTrace();
//                        }
                        skm.dbNewList(playlistName);
                    }
                });
                builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.cancel();
                    }
                });
                builder.show();

                listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                    @Override
                    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
//                        int num = 0;
//                        if(num == 0){
//                            skm.dbNewList(playlistName, skFile.get(position));
//                            num++;
//                        }else {
                            skm.dbUpdateList(1, playlistName, skFile.get(position));
//                        }
                    }
                });
            }
        };

        shuffleButton.setOnClickListener(shuffleClick);
        updateButton.setOnClickListener(updateClick);
        playlistButton.setOnClickListener(playlistClick);
        newPlaylistButton.setOnClickListener(newPlaylistClick);

        return rootView;
    }

    public void showDisplay(){

    }

    public void skSetIpHost(String host, int port){
        hostName = host;
        portNum = port;
        Log.d("IP/HOST", hostName + "/" + portNum);
    }

    public ArrayList<SKFile> shuffle(ArrayList<SKFile> list){
        Collections.shuffle(list);
        return list;
    }

    public int buildLibrary(String path){
        HttpURLConnection conn = null;
        MainActivity main = (MainActivity)getActivity();
        BufferedReader br;
        List<String> lines;
        String[] songsLines;
        byte[] buffer = new byte[4096];
        int bytesRead;
        int fileLength;

        try {
            URL tempUrl = new URL(main.getURL() + "/directory.txt");
            conn = (HttpURLConnection)tempUrl.openConnection();
            conn.setRequestMethod("GET");
            conn.setConnectTimeout(5000);
            conn.setReadTimeout(5000);

            if (conn.getResponseCode() == HttpURLConnection.HTTP_OK) {
                br = new BufferedReader(new InputStreamReader(tempUrl.openStream()));
                String s;
                lines = new ArrayList<>();
                while ((s = br.readLine()) != null){
                    lines.add(s);
                    System.out.println(s);
                }
                br.close();
                System.out.println("File Successfully downloaded");
            }else{
                System.out.println("Can't find file");
                return 2;
            }

        }catch(IOException e){
            e.printStackTrace();
            return 1;
        }

        for(String x : lines){
            String[] skData = x.split(" &%& ");
            SKFile skf = new SKFile(skData[0], Integer.parseInt(skData[1]), skData[2], skData[3], skData[4], Float.parseFloat(skData[5]));
            System.out.println(skData[5]);
            skFile.add(skf);
            skLibrary.add(skf);
        }
        return 0;
    }

    public int checkFile(int index){
        try {
            MainActivity main = (MainActivity) getActivity();
            String url = main.getURL() + "/" + skLibrary.get(index).getFilePath();
            URL fixedURL = new URL(url.replaceAll("\\s", "%20"));
            System.out.println(url);
            HttpURLConnection conn = (HttpURLConnection) fixedURL.openConnection();
            conn.setRequestMethod("HEAD");
            conn.setConnectTimeout(5000);
            conn.setReadTimeout(5000);
            if(conn.getResponseCode() == 200){
                songURL = fixedURL.toString();
                return 0;
            }
        }catch(IOException e){
            e.printStackTrace();
        }
        return 1;
    }

    private int skOpen(){
        try{
            sock = new Socket();
            sock.connect(new InetSocketAddress(hostName, portNum), 5000);
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
            dIS.readFully(buffer);
//            if(dIS.read(buffer) < buffer.length) {
//                System.out.println(dIS.read(buffer));
//            }
            //Log.d("RECEIVE", new String(buffer));
            //is.close();
        }catch(IOException e){
            e.printStackTrace();
        }
        return buffer;
    }

    public int skUIFile(int index)throws IOException{
        int con;
        byte[] ansData;
        String ans;
        SKFile temp;

//        if(skCacheCheck(index)){
//            temp = cache.get(index);
//            cache.remove(index);
//            cache.add(temp);
//            return 0;
//        }
        con = skOpen();
        if(con == 0){
            skSend("file");
            ansData = skRecieve();
            if(ansData != null){
                ans = new String(ansData);
                if(ans.equals("okay")){
                    return skRCVFileIndex(index);
                }else{
                    return -5;
                }
            }else{
                return -5;
            }
            //skClose();
        }
        return -5;
    }

    public int skRCVFileIndex(int index) throws IOException{
        String name ;
        String path = "";
        byte[] fileData;

        MainActivity main = (MainActivity)getActivity();
        if(!sockStatus){
            skOpen();
        }
        skSend(Integer.toString(index));
        fileData = skRecieve();
        try{
            name = skLibrary.get(index).getSongIndex() + ".mp3";
            songPath = name;
            songFile = new File(getActivity().getFilesDir(), name);
            try {
                Log.i("FILEPATH", "Path: " + songFile.getCanonicalPath());
            }catch(IOException e){
                e.printStackTrace();
            }
        }catch(Exception e) {
           e.printStackTrace();
        }
        Log.d("FILE DATA", fileData.length + "");
        if(fileData.length != 0){
            //songPath = dirPath + "\\" + name;
//            p = Paths.get(dirPath + name);
//            if(Files.notExists(p)){
//                new File(path).mkdirs();
//            }
            FileOutputStream fos = new FileOutputStream(songFile);
            fos.write(fileData);
            System.out.println(songFile);
            fos.close();
            skLibrary.get(index).skAddPath(path);
//            if (cache.size() > CACHEMAX) {
//                file = cache.remove(0);
//                appContext.deleteFile(file.getCachePath());
//            }
            cache.add(skLibrary.get(index));
            skClose();
            return 0;
        }else {
            skClose();
            return 1;
        }
    }

    public int userComm(String command) throws IOException{
        int val;
        byte[] data;
        String[] skData;
        String dataString;
        SKFile sk;
        if(command.equals("update")){
            val = skOpen();
            if(val == 1) {
                Log.e("OPEN", "Error connecting to server");
                return 1;
            }
            skSend("ls");
            data = skRecieve();
            dataString = new String(data);
            //System.out.println(dataString);
            directory = dataString.split("\n");
            skFile.clear();
            for(String x: directory){
                skData = x.split("&%&");
                //System.out.println(x);
                if(skData.length == 5) {
                    sk = new SKFile(skData[0], Integer.parseInt(skData[1]),
                            skData[2], skData[3], skData[4], Float.parseFloat(skData[5]));
                    skFile.add(sk);
                    skLibrary.add(sk);
                }

            }
            skClose();
        }else if(command == "ls"){
            int i = 0;
            while (i < directory.length){
                System.out.println(i + ": " + directory[i]);
                i++;
            }
        }else if(command == "file"){
            val = skOpen();
            if(val == 1) {
                Log.e("OPEN", "Error Contacting Server");
                return 1;
            }
        }
        return 0;
    }

    private class UpdateTask extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... params) {
            byte[] fileData;
            skSetIpHost(hostName, portNum);
            buildLibrary("directory.txt");
            return null;
        }
    }

    private class PlaySong extends AsyncTask<Void, Void, Void>{

        @Override
        protected Void doInBackground(Void... params){
            System.out.println(checkFile(index));
            return null;
        }
    }
    // TODO: Rename method, update argument and hook method into UI event
//    public void onButtonPressed(Uri uri) {
//        if (mListener != null) {
//            mListener.onFragmentInteraction(uri);
//        }
//    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
//        if (context instanceof OnFragmentInteractionListener) {
//            mListener = (OnFragmentInteractionListener) context;
//        } else {
//            throw new RuntimeException(context.toString()
//                    + " must implement OnFragmentInteractionListener");
//        }
    }

    @Override
    public void onDetach() {
        super.onDetach();
        mListener = null;
    }

    /**
     * This interface must be implemented by activities that contain this
     * fragment to allow an interaction in this fragment to be communicated
     * to the activity and potentially other fragments contained in that
     * activity.
     * <p>
     * See the Android Training lesson <a href=
     * "http://developer.android.com/training/basics/fragments/communicating.html"
     * >Communicating with Other Fragments</a> for more information.
     */
    public interface OnFragmentInteractionListener {
        // TODO: Update argument type and name
        void onFragmentInteraction(Uri uri);
    }
}