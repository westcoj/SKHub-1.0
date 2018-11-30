package com.sk.krolikj.skandroid;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

public class MyDatabaseHelper extends SQLiteOpenHelper {

    private static final String DB_NAME = "playlists.db";
//    private static final String COL_1 = "Path";
//    private static final String COL_2 = "SongDex";
//    private static final String COL_3 = "Title";
//    private static final String COL_4 = "Artist";
//    private static final String COL_5 = "Album";

    private String DATABASE_CREATE = "CREATE TABLE IF NOT EXISTS New_Playlist(\n" +
            "    path text UNIQUE NOT NULL,\n" +
            "    songDex integer PRIMARY KEY,\n" +
            "    title text,\n" +
            "    artist text,\n" +
            "    album text,\n" +
            "    duration integer\n" +
            "    )";

    public MyDatabaseHelper(Context context) {
        super(context, DB_NAME, null, 1);
        SQLiteDatabase db = this.getWritableDatabase();
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(DATABASE_CREATE);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
//        db.execSQL("DROP TABLE IF EXISTS MyEmployees");
//        onCreate(db);
    }
}
