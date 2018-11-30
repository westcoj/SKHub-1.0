package com.sk.krolikj.skandroid;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
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

    private Connection connect() {
        try {
            System.out.println(dbPath);
            Connection conn = DriverManager.getConnection(dbPath);
            System.out.println("Connection to SQLite established");
            return conn;
        } catch (SQLException e) {
            e.getErrorCode();
        }
        return null;
    }

    public SQLiteDatabase createDb(){
        db = actContext.openOrCreateDatabase("playlists", Context.MODE_PRIVATE, null);
        return db;
    }

    private String scrubName(String name) {
        return name.replaceAll(" ", "_");
    }

    private ArrayList<SKFile> query(String name) {
        ArrayList<SKFile> list = new ArrayList<>();
//        try {
//            Connection conn = connect();
//            if(conn == null){
//
//            }
//            Statement stm = conn.createStatement();
//            ResultSet rs = stm.executeQuery(name);
//            while (rs.next()) {
//                SKFile sk = new SKFile(rs.getString("path"), rs.getInt("songDex"),
//                        rs.getString("title"), rs.getString("artist"),
//                        rs.getString("album"));
//                list.add(sk);
//            }
//        } catch (SQLException e) {
//            e.getErrorCode();
//        }
        return list;
    }

    public ArrayList<SKFile> getDataBaseList(String name) {
        ArrayList<SKFile> list = new ArrayList<>();
        Cursor resultSet = db.rawQuery("SELECT path, songDex, title, artist, album FROM " + scrubName(name), null);
        while(resultSet.moveToNext()) {
            SKFile sk = new SKFile(resultSet.getString(0), resultSet.getInt(1), resultSet.getString(2),
                    resultSet.getString(3), resultSet.getString(4));
            list.add(sk);
        }
        return list;
    }

    public ArrayList<SKFile> dbGetAll() {
        //String getAll = "SELECT name FROM sqlite_master WHERE type='table';";
        ArrayList<SKFile> list = new ArrayList<>();
        Cursor resultSet = db.rawQuery("SELECT name FROM sqlite_master \n" +
                "WHERE type='table' and name <> 'android_metadata'\n" +
                "ORDER BY name;", null);
        while(resultSet.moveToNext()){
            SKFile sk = new SKFile(resultSet.getString(0), -5, null, null, null);
            list.add(sk);
        }
        return list;
    }

    public void dbNewList(String name) {
        String table = "CREATE TABLE IF NOT EXISTS " + scrubName(name) + "(\n" +
                "    path text UNIQUE NOT NULL,\n" +
                "    songDex integer PRIMARY KEY,\n" +
                "    title text,\n" +
                "    artist text,\n" +
                "    album text\n" +
//                "    duration integer\n" +
                "    );";
//        try {
//        System.out.println(skf.getSongTitle());
//        String[] songArray = new String[5];
//        songArray[0] = skf.getFilePath();
//        songArray[1] = Integer.toString(skf.getSongIndex());
//        songArray[2] = skf.getSongTitle();
//        songArray[3] = skf.getSongArtist();
//        songArray[4] = skf.getSongAlbum();
        db.execSQL(table);
        System.out.println("Song Added");
//            Connection conn = connect();
//            System.out.println("Connect Error: " + conn);
//            Statement stm = conn.createStatement();
//            stm.execute(table);
//            conn.commit();
//            conn.close();
//        } catch (SQLException e) {
//            e.getErrorCode();
//        }
    }

    public void dbRemoveList(String name) {
        String remove = "DROP TABLE IF EXISTS " + scrubName(name);
        db.execSQL(remove);
    }

    public void dbUpdateList(int op, String name, SKFile skf) {
        Connection conn = connect();
        if (op == 1) {
            String add = "INSERT INTO " + scrubName(name) +
                    " (path, songDex, title, artist, album) VALUES (?,?,?,?,?)";

            String[] songArray = new String[5];
            songArray[0] = skf.getFilePath();
            songArray[1] = Integer.toString(skf.getSongIndex());
            songArray[2] = skf.getSongTitle();
            songArray[3] = skf.getSongArtist();
            songArray[4] = skf.getSongAlbum();

            ContentValues insertVals = new ContentValues();
            insertVals.put("path", songArray[0]);
            insertVals.put("songDex", songArray[1]);
            insertVals.put("title", songArray[2]);
            insertVals.put("artist", songArray[3]);
            insertVals.put("album", songArray[4]);
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