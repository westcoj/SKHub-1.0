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

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collections;
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
    private ListView listView;
    private int portNum;
    private String hostName;
    private String dirPath;
    private String playlistName;
    private ArrayList<SKFile> skFile;
    private ArrayList<SKFile> skLibrary;
    private Button updateButton;
    private Button shuffleButton;
    private Button playlistButton;
    private Button newPlaylistButton;
    private int index;
    private SKMedia skm;
    private String songURL;


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

        skFile = new ArrayList<>();
        skLibrary = new ArrayList<>();

        if(main.getURL() != null) {
            dirPath = main.getDirectoryPath();

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

                    main.setSkFile(skFile);
                    main.setSongURL(songURL);
                    final FragmentTransaction ft = getFragmentManager().beginTransaction();
                    ft.replace(R.id.mainFrame, new PlayerFragment());
                    ft.commit();
                }
            });
        }

        View.OnClickListener updateClick = new View.OnClickListener() {
            @Override
            public void onClick(View v){
                dirPath = main.getDirectoryPath();
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

                        final FragmentTransaction ft = getFragmentManager().beginTransaction();
                        ft.replace(R.id.mainFrame, new PlayerFragment());
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
                        main.setSkFile(skFile);
                        main.setSongURL(songURL);
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
                        skFile.clear();
                        skFile = skm.getDataBaseList(tempList.get(position).getFilePath());
                        final ListAdapter songAdapter = new ListAdapter(getActivity(), skFile);
                        listView.setAdapter(songAdapter);
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
                        skm.dbUpdateList(1, playlistName, skFile.get(position));
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
        HttpURLConnection conn;
        MainActivity main = (MainActivity)getActivity();
        BufferedReader br;
        List<String> lines;

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

    private class UpdateTask extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... params) {
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