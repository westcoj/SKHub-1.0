package com.sk.krolikj.skandroid;

import android.content.Context;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.SeekBar;
import android.widget.TextView;

import java.io.IOException;
import java.util.ArrayList;

public class PlayerFragment extends Fragment {

    private Button playButton;
    private Button nextButton;
    private Button lastButton;
    private SeekBar positionBar;
    private SeekBar volumeBar;
    private TextView timePassedLabel;
    private TextView timeLeftLabel;
    private TextView songName;
    private static MediaPlayer mp;
    private ArrayList<SKFile> songList;
    private SKFile skf;
    private float songLength;
    final static String ARG_POSITION = "position";
    int mCurrentPosition = -1;
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    private OnFragmentInteractionListener mListener;

    public PlayerFragment() {
        // Required empty public constructor
    }

    public static PlayerFragment newInstance(String param1, String param2) {
        PlayerFragment fragment = new PlayerFragment();
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
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

        if (savedInstanceState != null) {
            mCurrentPosition = savedInstanceState.getInt(ARG_POSITION);
        }
//        if (container != null) {
//            container.removeAllViews();
//        }

        final MainActivity main = (MainActivity)getActivity();
        ImageView logo = main.findViewById(R.id.Logo);
        ImageView sounderkin = main.findViewById(R.id.SounderKin);
        logo.setVisibility(View.GONE);
        sounderkin.setVisibility(View.GONE);

        View rootView = inflater.inflate(R.layout.fragment_player, container, false);

        playButton = rootView.findViewById(R.id.playButton);
        nextButton = rootView.findViewById(R.id.nextButton);
        lastButton = rootView.findViewById(R.id.lastButton);
        timePassedLabel = rootView.findViewById(R.id.timePassedLabel);
        timeLeftLabel = rootView.findViewById(R.id.timeLeftLabel);
        songName = rootView.findViewById(R.id.songName);
        skf = main.getSongData();
//        songName.setText(skf.getSongTitle());
//        songLength = skf.getSongTime();
        System.out.println(songLength);
        songList = main.getSkFile();
        try {
            songName.setText(skf.getSongTitle());
            songLength = skf.getSongTime();
            //mp = MediaPlayer.create(getActivity().getBaseContext(), R.raw.song);
            //mp = MediaPlayer.create(getActivity().getBaseContext(), Uri.fromFile(main.getSong()));
            mp = new MediaPlayer();
            mp.setAudioStreamType(AudioManager.STREAM_MUSIC);
            //mp.seekTo(0);
            mp.setVolume(0.5f, 0.5f);
            mp.setDataSource(main.getSongURL());
            mp.prepare();
            //mp.start();
            //playButton.setBackgroundResource(R.drawable.ic_baseline_pause_24px);
        } catch (IOException | NullPointerException e) {
            System.out.println("No song chosen my dude");
        }

        playButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (!mp.isPlaying()) {
                    mp.start();
                    playButton.setBackgroundResource(R.drawable.ic_baseline_pause_24px);
                } else {
                    mp.pause();
                    playButton.setBackgroundResource(R.drawable.ic_baseline_play_arrow_24px);
                }
            }
        });

        nextButton.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                int index;
                if(mp.isPlaying())
                    mp.stop();
                index = songList.indexOf(skf);
                if(index+1 == songList.size())
                    index = -1;
                skf = songList.get(index+1);
                String newURL = main.getURL() + "/" + skf.getFilePath();
                songName.setText(skf.getSongTitle());
                try {
                    String fixedUrl = newURL.replaceAll("\\s", "%20");
                    mp = new MediaPlayer();
                    mp.setDataSource(fixedUrl);
                    mp.prepare();
                    mp.start();
                    playButton.setBackgroundResource(R.drawable.ic_baseline_pause_24px);
                }catch(IOException e){
                    e.printStackTrace();
                }
            }
        });

        lastButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int index;
                if(mp.getCurrentPosition() < 5000) {
                    if (mp.isPlaying())
                        mp.stop();
                    index = songList.indexOf(skf);
                    if (index - 1 < 0)
                        index = songList.size();
                    skf = songList.get(index - 1);
                    String newURL = main.getURL() + "/" + skf.getFilePath();
                    songName.setText(skf.getSongTitle());
                    try {
                        String fixedUrl = newURL.replaceAll("\\s", "%20");
                        mp = new MediaPlayer();
                        mp.setDataSource(fixedUrl);
                        mp.prepare();
                        mp.start();
                        playButton.setBackgroundResource(R.drawable.ic_baseline_pause_24px);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }else{
                    mp.pause();
                    mp.seekTo(0);
                    mp.start();
                }
            }
        });

        positionBar = rootView.findViewById(R.id.songPositionBar);
        positionBar.setMax((int)songLength);
        positionBar.setOnSeekBarChangeListener(
                new SeekBar.OnSeekBarChangeListener() {
                    @Override
                    public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                        if (fromUser) {
                            mp.seekTo(progress);
                            positionBar.setProgress(progress);

                        }
                    }

                    @Override
                    public void onStartTrackingTouch(SeekBar seekBar) {

                    }

                    @Override
                    public void onStopTrackingTouch(SeekBar seekBar) {

                    }
                }
        );

        volumeBar = rootView.findViewById(R.id.volumeBar);
        volumeBar.setOnSeekBarChangeListener(
                new SeekBar.OnSeekBarChangeListener() {
                    @Override
                    public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                        float volumeLvl = progress / 100f;
                        mp.setVolume(volumeLvl, volumeLvl);
                    }

                    @Override
                    public void onStartTrackingTouch(SeekBar seekBar) {

                    }

                    @Override
                    public void onStopTrackingTouch(SeekBar seekBar) {

                    }
                }
        );

        new Thread(new Runnable() {
            @Override
            public void run() {
                while (mp != null) {
                    try {
                        Message msg = new Message();
                        msg.what = mp.getCurrentPosition();
                        handler.sendMessage(msg);
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();
        return rootView;
    }

    private Handler handler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            int curPosition = msg.what;
            positionBar.setProgress(curPosition);
            String passedTime = timeLabel(curPosition);
            timePassedLabel.setText(passedTime);
            String timeLeft = timeLabel((int)songLength - curPosition);
            timeLeftLabel.setText("-" + timeLeft);
        }
    };

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
    }

    @Override
    public void onPause() {
        super.onPause();
        if(mp.isPlaying())
            mp.stop();
    }

    @Override
    public void onDetach() {
        super.onDetach();
        mListener = null;
    }

    @Override
    public void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);

        // Save the current article selection in case we need to recreate the fragment
        outState.putInt(ARG_POSITION, mCurrentPosition);
    }

    public interface OnFragmentInteractionListener {
        // TODO: Update argument type and name
        void onFragmentInteraction(Uri uri);
    }

    public String timeLabel(int time) {
        String stringTime;
        int minutes = time / 1000 / 60;
        int seconds = (time / 1000) - (minutes * 60);
        if (seconds < 10)
            stringTime = minutes + ":0" + seconds;
        else
            stringTime = minutes + ":" + seconds;
        return stringTime;
    }
}