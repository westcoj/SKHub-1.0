package com.sk.krolikj.skandroid;

import android.content.Context;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.design.widget.TextInputLayout;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;

import java.lang.*;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.Socket;
import java.net.URL;
import java.util.concurrent.ExecutionException;


public class ConfigFragment extends Fragment {

    private int portNum;
    private String ip;
    private URL url;
    private Boolean connectSuccess = false;
    private TextInputLayout ipInput;
    private TextInputLayout portInput;
    private Button connectButton;
    private String ARG_POSITION = "position";
    private int mCurrentPosition = -1;
    private static final String host = "hostname";
    private static final String ipAd = "portnum";

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

    public void skSetIpHost(String host, int port) {
        ip = host;
        portNum = port;
        Log.d("IP/HOST", ip + "/" + portNum);
    }

    private int skOpen() {
        try {
            MainActivity main = (MainActivity)getActivity();
            url = new URL("http://" + ip + ":" + portNum + "/hello");
            System.out.println("URL: " + url.toString());
            HttpURLConnection conn = (HttpURLConnection)url.openConnection();
            conn.setRequestMethod("HEAD");
            conn.setConnectTimeout(5000);
            conn.setReadTimeout(5000);
            System.out.println(conn.getResponseCode());
            url = new URL("http://" + ip + ":" + portNum);
            main.setURL(url);
            return 0;
        } catch (IOException e) {
            e.printStackTrace();
            return 1;
        }
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

//        if (container != null) {
//            container.removeAllViews();
//        }
        final View rootView = inflater.inflate(R.layout.fragment_config, container, false);

        MainActivity main = (MainActivity)getActivity();
        ImageView logo = main.findViewById(R.id.Logo);
        ImageView sounderkin = main.findViewById(R.id.SounderKin);
        logo.setVisibility(View.GONE);
        sounderkin.setVisibility(View.GONE);

        connectButton = rootView.findViewById(R.id.connectButton);
        connectButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ipInput = rootView.findViewById(R.id.ipInputBox);
                portInput = rootView.findViewById(R.id.portInputBox);
                MainActivity main = (MainActivity)getActivity();
                String ipNum = ipInput.getEditText().getText().toString();
                String port = portInput.getEditText().getText().toString();
                if(port.equals("") || ipNum.equals("")) {
                }else {
                    ip = ipNum;
                    portNum = Integer.parseInt(port);

                    try {
                        new ConfigFragment.ConnectTask().execute().get();
                        main.skSetIpHost(ip, portNum);
                        main.setURL(url);
                    } catch (ExecutionException | InterruptedException ex) {
                        ex.printStackTrace();
                    }
                }
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
                System.out.println("Connection Successful");
            } else {
                connectSuccess = false;
                System.out.println("Connection Failed");
            }
            return null;
        }
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
    }

    @Override
    public void onDetach() {
        super.onDetach();
    }

//    public interface OnFragmentInteractionListener {
//        // TODO: Update argument type and name
//        void onFragmentInteraction(Uri uri);
//    }
}