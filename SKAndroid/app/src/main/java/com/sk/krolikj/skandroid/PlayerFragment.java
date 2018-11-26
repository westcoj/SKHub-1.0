package com.sk.krolikj.skandroid;

import android.content.Context;
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
import android.widget.SeekBar;
import android.widget.TextView;

public class PlayerFragment extends Fragment {

    Button playButton;
    SeekBar positionBar;
    SeekBar volumeBar;
    TextView timePassedLabel;
    TextView timeLeftLabel;
    MediaPlayer mp;
    int songLength;
    final static String ARG_POSITION = "position";
    int mCurrentPosition = -1;
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    private String mParam1;
    private String mParam2;

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
        if (getArguments() != null) {
            mParam1 = getArguments().getString(ARG_PARAM1);
            mParam2 = getArguments().getString(ARG_PARAM2);
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

        if (savedInstanceState != null) {
            mCurrentPosition = savedInstanceState.getInt(ARG_POSITION);
        }

        View rootView = inflater.inflate(R.layout.fragment_player, container, false);

        playButton = rootView.findViewById(R.id.playButton);
        timePassedLabel = rootView.findViewById(R.id.timePassedLabel);
        timeLeftLabel = rootView.findViewById(R.id.timeLeftLabel);
        MainActivity main = (MainActivity)getActivity();

        //mp = MediaPlayer.create(getActivity().getBaseContext(), R.raw.song);
        mp = MediaPlayer.create(getActivity().getBaseContext(), Uri.fromFile(main.getSong()));
        System.out.println(main.getSong());
        mp.setLooping(true);
        mp.seekTo(0);
        mp.setVolume(0.5f, 0.5f);
        songLength = mp.getDuration();

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

        positionBar = rootView.findViewById(R.id.songPositionBar);
        positionBar.setMax(songLength);
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
            String timeLeft = timeLabel(songLength - curPosition);
            timeLeftLabel.setText("-" + timeLeft);
        }
    };

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