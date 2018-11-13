package com.sk.krolikj.skandroid;

import android.content.Intent;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.os.PersistableBundle;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;

public class PlayerActivity extends AppCompatActivity {

    Button playButton;
    SeekBar positionBar;
    SeekBar volumeBar;
    TextView timePassedLabel;
    TextView timeLeftLabel;
    MediaPlayer mp;
    int songLength;


    @Override
    public void onCreate(@Nullable Bundle savedInstanceState){//, @androidx.annotation.Nullable PersistableBundle persistentState) {
        super.onCreate(savedInstanceState);//, persistentState);
        setContentView(R.layout.player_activity);

        BottomNavigationView navigation = findViewById(R.id.navigation);
        Menu menu = navigation.getMenu();
        MenuItem menuItem = menu.getItem(1);
        menuItem.setChecked(true);

        BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
                = new BottomNavigationView.OnNavigationItemSelectedListener() {

            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                switch (item.getItemId()) {
                    case R.id.navigation_library:
                        Intent intent = new Intent(PlayerActivity.this, MainActivity.class);
                        startActivity(intent);
                        return true;
                    case R.id.navigation_player:

                        return true;
                    case R.id.navigation_config:
                        Intent intent1 = new Intent(PlayerActivity.this, ConfigActivity.class);
                        startActivity(intent1);
                        return true;
                }
                return false;
            }
        };
        navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);

        playButton = findViewById(R.id.playButton);
        timePassedLabel = findViewById(R.id.timePassedLabel);
        timeLeftLabel = findViewById(R.id.timeLeftLabel);

        mp = MediaPlayer.create(this,R.raw.song);
        mp.setLooping(true);
        mp.seekTo(0);
        mp.setVolume(0.5f, 0.5f);
        songLength = mp.getDuration();

        positionBar = findViewById(R.id.songPositionBar);
        positionBar.setMax(songLength);
        positionBar.setOnSeekBarChangeListener(
                new SeekBar.OnSeekBarChangeListener() {
                    @Override
                    public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                        if(fromUser){
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

        volumeBar = findViewById(R.id.volumeBar);
        volumeBar.setOnSeekBarChangeListener(
                new SeekBar.OnSeekBarChangeListener(){
                    @Override
                    public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser){
                        float volumeLvl = progress / 100f;
                        mp.setVolume(volumeLvl, volumeLvl);
                    }

                    @Override
                    public void onStartTrackingTouch(SeekBar seekBar){

                    }

                    @Override
                    public void onStopTrackingTouch(SeekBar seekBar){

                    }
                }
        );

        new Thread(new Runnable() {
            @Override
            public void run() {
                while(mp != null){
                    try {
                        Message msg = new Message();
                        msg.what = mp.getCurrentPosition();
                        handler.sendMessage(msg);
                        Thread.sleep(1000);
                    }catch(InterruptedException e){
                        e.printStackTrace();
                    }
                }
            }
        }).start();
    }

    private Handler handler = new Handler(){
        @Override
        public void handleMessage(Message msg){
            int curPosition = msg.what;
            positionBar.setProgress(curPosition);
            String passedTime = timeLabel(curPosition);
            timePassedLabel.setText(passedTime);
            String timeLeft = timeLabel(songLength-curPosition);
            timeLeftLabel.setText("-" + timeLeft);
        }
    };

    public String timeLabel(int time){
        String stringTime;
        int minutes = time/1000/60;
        int seconds = (time/1000) - (minutes*60);
        if(seconds < 10)
            stringTime = minutes + ":0" + seconds;
        else
            stringTime = minutes + ":" + seconds;
        return stringTime;
    }

    public void playButtonClick(View view){
        if(!mp.isPlaying()) {
            mp.start();
            playButton.setBackgroundResource(R.drawable.ic_baseline_pause_24px);
        }else{
            mp.pause();
            playButton.setBackgroundResource(R.drawable.ic_baseline_play_arrow_24px);
        }
    }
}
