package com.sk.krolikj.skandroid;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.util.ArrayList;

public class SKMedia {

    private MyDatabaseHelper myDbHelper;
    private SQLiteDatabase db;
    private String dbPath;
    private Context actContext;

    public SKMedia(Context context) {
       // myDbHelper = new MyDatabaseHelper(context);
        //db = myDbHelper.getWritableDatabase();
        actContext = context;
        dbPath = actContext.getDatabasePath("playlists.db").toString();
    }

    public SQLiteDatabase createDb(){
        db = actContext.openOrCreateDatabase("playlists", Context.MODE_PRIVATE, null);
        return db;
    }

    private String scrubName(String name) {
        return name.replaceAll(" ", "_");
    }


    public ArrayList<SKFile> getDataBaseList(String name) {
        ArrayList<SKFile> list = new ArrayList<>();
        Cursor resultSet = db.rawQuery("SELECT path, songDex, title, artist, album, duration FROM " + scrubName(name), null);
        while(resultSet.moveToNext()) {
            SKFile sk = new SKFile(resultSet.getString(0), resultSet.getInt(1), resultSet.getString(2),
                    resultSet.getString(3), resultSet.getString(4), resultSet.getFloat(5));
            list.add(sk);
        }
        resultSet.close();
        return list;
    }

    public ArrayList<SKFile> dbGetAll() {
        ArrayList<SKFile> list = new ArrayList<>();
        Cursor resultSet = db.rawQuery("SELECT name FROM sqlite_master \n" +
                "WHERE type='table' and name <> 'android_metadata'\n" +
                "ORDER BY name;", null);
        while(resultSet.moveToNext()){
            SKFile sk = new SKFile(resultSet.getString(0), -5, null, null, null, 0);
            list.add(sk);
        }
        resultSet.close();
        return list;
    }

    public void dbNewList(String name) {
        String table = "CREATE TABLE IF NOT EXISTS " + scrubName(name) + "(\n" +
                "    path text UNIQUE NOT NULL,\n" +
                "    songDex integer PRIMARY KEY,\n" +
                "    title text,\n" +
                "    artist text,\n" +
                "    album text\n" +
                "    duration integer\n" +
                "    );";

        db.execSQL(table);
        System.out.println("Song Added");
    }

    public void dbRemoveList(String name) {
        String remove = "DROP TABLE IF EXISTS " + scrubName(name);
        db.execSQL(remove);
    }

    public void dbUpdateList(int op, String name, SKFile skf) {
        if (op == 1) {
            String[] songArray = new String[6];
            songArray[0] = skf.getFilePath();
            songArray[1] = Integer.toString(skf.getSongIndex());
            songArray[2] = skf.getSongTitle();
            songArray[3] = skf.getSongArtist();
            songArray[4] = skf.getSongAlbum();
            songArray[5] = Float.toString(skf.getSongTime());

            ContentValues insertVals = new ContentValues();
            insertVals.put("path", songArray[0]);
            insertVals.put("songDex", songArray[1]);
            insertVals.put("title", songArray[2]);
            insertVals.put("artist", songArray[3]);
            insertVals.put("album", songArray[4]);
            insertVals.put("duration", songArray[5]);
            db.insert(scrubName(name), null, insertVals);

        } else {
//            try {
//                Statement stm = conn.createStatement();
//                int index = skf.getSongIndex();
//                String remove = "DELETE FROM " + scrubName(name) + " WHERE songDex=?;";
//                stm.execute(remove, index);
//                conn.commit();
//                conn.close();
//            } catch (SQLException e) {
//                e.getErrorCode();
//            }
        }
    }
}