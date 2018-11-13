package com.sk.krolikj.skandroid;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.design.widget.BottomNavigationView;
import android.support.design.widget.TextInputLayout;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import java.lang.*;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.concurrent.ExecutionException;


public class ConfigFragment extends Fragment {

    private int portNum;
    private String ip;
    private Socket sock;
    private DataInputStream dIS;
    private DataOutputStream dOS;
    private Boolean connectSuccess = false;
    private TextInputLayout ipInput;
    private TextInputLayout portInput;
    private Button connectButton;
    private String ARG_POSITION = "position";
    private int mCurrentPosition = -1;
    private static final String host = "hostname";
    private static final String ipAd = "portnum";

    private String mParam1;
    private String mParam2;

    private OnFragmentInteractionListener mListener;

    public ConfigFragment() {
        // Required empty public constructor
    }

    public static ConfigFragment newInstance(String param1, String param2) {
        ConfigFragment fragment = new ConfigFragment();
        Bundle args = new Bundle();
        args.putString(host, param1);
        args.putString(ipAd, param2);
        fragment.setArguments(args);
        return fragment;
    }

    public Boolean getConnectSuccess() {
        return connectSuccess;
    }

    public void skSetIpHost(String host, int port) {
        ip = host;
        portNum = port;
        Log.d("IP/HOST", ip + "/" + portNum);
    }

    private int skOpen() {
        try {
            sock = new Socket();
            sock.connect(new InetSocketAddress(ip, portNum), 5000);
            dIS = new DataInputStream(sock.getInputStream());
            dOS = new DataOutputStream(sock.getOutputStream());
            Log.d("OPEN", "Connection Established");
            return 0;
        } catch (IOException e) {
            Log.e("!OPEN", e.toString());
            return 1;
        }
    }

    private void skClose() throws IOException {
        sock.close();
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

        final View rootView = inflater.inflate(R.layout.fragment_config, container, false);

        connectButton = rootView.findViewById(R.id.connectButton);
        connectButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ipInput = rootView.findViewById(R.id.ipInputBox);
                portInput = rootView.findViewById(R.id.portInputBox);
                String ipNum = ipInput.getEditText().getText().toString();
                String port = portInput.getEditText().getText().toString();
                ip = ipNum;
                portNum = Integer.parseInt(port);
                try {
                    new ConfigFragment.ConnectTask().execute().get();
                }catch(ExecutionException | InterruptedException ex){
                    ex.printStackTrace();
                }
                MainActivity main = (MainActivity)getActivity();
                main.setHostPort(ipNum, port);
                //Bundle args = new Bundle();
                //args.putString("network", ip + "/" + portNum);
                //homeFrag.setArguments(args);
                //getFragmentManager().beginTransaction().add(R.id.mainFrame, homeFrag).commit();

            }
        });

        return rootView;
    }

    @Override
    public void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);

        // Save the current article selection in case we need to recreate the fragment
        outState.putInt(ARG_POSITION, mCurrentPosition);
    }

    private class ConnectTask extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... params) {
            System.out.println(ip + "/" + portNum);
            skSetIpHost(ip, portNum);
            if (skOpen() == 0) {
                connectSuccess = true;
                try {
                    skClose();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                return null;
            } else {
                connectSuccess = false;

                return null;
            }
        }
    }

    public void onButtonPressed(Uri uri) {
        if (mListener != null) {
            mListener.onFragmentInteraction(uri);
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

    public interface OnFragmentInteractionListener {
        // TODO: Update argument type and name
        void onFragmentInteraction(Uri uri);
    }
}
