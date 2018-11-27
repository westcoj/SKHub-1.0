package com.sk.krolikj.skandroid;

import android.app.Activity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.ArrayList;

public class ListAdapter extends ArrayAdapter {

    private Activity context;
    private ArrayList<SKFile> mData;
    private int imageId;

    public ListAdapter(Activity context, ArrayList<SKFile> aList){

        super(context,R.layout.listview_row, aList);
        this.context = context;
        mData = aList;
    }

    public View getView(int position, View view, ViewGroup parent) {
        LayoutInflater inflater = context.getLayoutInflater();
        View rowView = inflater.inflate(R.layout.listview_row, null, true);

        TextView songTextField = rowView.findViewById(R.id.songName);
        TextView artistTextField = rowView.findViewById(R.id.artist_album);
        ImageView imageView = rowView.findViewById(R.id.artwork_icon);

        songTextField.setText(mData.get(position).getSongTitle());
        artistTextField.setText(mData.get(position).getSongArtist());

        return rowView;
    }

}