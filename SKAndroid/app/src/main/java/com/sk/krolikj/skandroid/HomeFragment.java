package com.sk.krolikj.skandroid;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ListView;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.util.ArrayList;
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
    ListView listView;
    private int portNum;
    private String hostName;
    private String dirPath;
    private boolean sockStatus;
    private Socket sock;
    private DataInputStream dIS;
    private DataOutputStream dOS;
    private String[] directory;
    private ArrayList<SKFile> skFile;
    private Context appContext;
    private ArrayList<SKFile> cache;
    private final static int CACHEMAX = 5;
    private Button updateButton;


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
//        if (getArguments() != null) {
//            mParam1 = getArguments().getString(ARG_PARAM1);
//            mParam2 = getArguments().getString(ARG_PARAM2);
//        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        final View rootView = inflater.inflate(R.layout.fragment_home, container, false);
        MainActivity main = (MainActivity)getActivity();
        String value = main.getHostPort();
        listView = rootView.findViewById(R.id.my_listview);
        updateButton = rootView.findViewById(R.id.updateButton);
        System.out.println(updateButton);

        View.OnClickListener updateClick = new View.OnClickListener() {
            @Override
            public void onClick(View v){
//                String value[] = getArguments().getStringArray("network");
//                hostName = value[0];
//                portNum = Integer.parseInt(value[1]);
                MainActivity main = (MainActivity)getActivity();
                String config = main.getHostPort();
                String[] str = config.split("/");
                hostName = str[0];
                portNum = Integer.parseInt(str[1]);
                skFile = new ArrayList<SKFile>();
                System.out.println(hostName + "/" + portNum);
                try {
                    new HomeFragment.UpdateTask().execute().get();
                }catch(InterruptedException | ExecutionException ex){
                    ex.printStackTrace();
                }
                for(SKFile x: skFile){
                    System.out.println(x.getSongTitle());
                }
                ListAdapter adapter = new ListAdapter(getActivity(), skFile);
                listView.setAdapter(adapter);
            }
        };
        System.out.println(updateClick);
        updateButton.setOnClickListener(updateClick);
//        updateButton.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                String ipNum = "192.168.1.78";
//                String port = "9222";
//                hostName = ipNum;
//                portNum = Integer.parseInt(port);
//                System.out.println(hostName + "/" + portNum);
//                new HomeFragment.UpdateTask().execute();
//                ListAdapter adapter = new ListAdapter(getActivity(), skFile);
//                listView.setAdapter(adapter);
//            }
//        });

        return rootView;
    }

    public void skSetIpHost(String host, int port){
        hostName = host;
        portNum = port;
        Log.d("IP/HOST", hostName + "/" + portNum);
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
        String name = "";
        String path = "";
        byte[] fileData;
        SKFile file;
        //Path p;

        if(!sockStatus){
            skOpen();
        }
        skSend(Integer.toString(index));
        fileData = skRecieve();
        try{
            name = skFile.get(index).getsongIndex() + ".mp3";
        }catch(Exception e) {
            Log.e("NAMING", e.toString());
        }
        Log.d("FILE DATA", fileData.length + "");
        if(fileData.length != 0){
            path = dirPath + "\\" + name;
//            p = Paths.get(dirPath + name);
//            if(Files.notExists(p)){
//                new File(path).mkdirs();
//            }
            FileOutputStream fos = new FileOutputStream(path);
            fos.write(fileData);
            fos.close();
            skFile.get(index).skAddPath(path);
            if(cache.size() > CACHEMAX){
                file = cache.remove(0);
                appContext.deleteFile(file.getCachePath());
            }
            cache.add(skFile.get(index));
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
            for(String x: directory){
                skData = x.split("&%&");
                //System.out.println(x);
                if(skData.length == 5) {
                    sk = new SKFile(skData[0], Integer.parseInt(skData[1]),
                            skData[2], skData[3], skData[4]);
                    skFile.add(sk);
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
        protected Void doInBackground(Void... params){
            byte[] fileData;
            skSetIpHost(hostName, portNum);
            //skOpen();
            //System.out.println(dirPath);
            try {
                userComm("update");
                skUIFile(0);
            } catch (IOException e) {
                Log.e("UIFILE", e.toString());
            }
            return null;
        }

        protected Void onPostExecute(long result){
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
