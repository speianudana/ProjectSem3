package com.example.skeez.camera;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.media.ImageWriter;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import com.otaliastudios.cameraview.CameraListener;
import com.otaliastudios.cameraview.CameraUtils;
import com.otaliastudios.cameraview.CameraView;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.OutputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;
import java.nio.ByteBuffer;


//import com.google.zxing.client.android.CaptureActivity;
//import com.google.zxing.client.android.camera.;
//import com.google.zxing.client.

public class MainActivity extends AppCompatActivity {
    CameraView camera;
    Context mContext;
    byte[] image;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        camera = findViewById(R.id.camera);
        camera.setLifecycleOwner(MainActivity.this);
        // From fragments, use fragment.viewLifecycleOwner instead of this!



        Button makePhotoButton = findViewById(R.id.makePhoto);
        Button sendImageButton = findViewById(R.id.sendImage);
        final ImageView imageView = findViewById(R.id.image);

        camera.addCameraListener(new CameraListener() {
            @Override
            public void onPictureTaken(final byte[] picture) {
                // Create a bitmap or a file...
                // CameraUtils will read EXIF orientation for you, in a worker thread.
                CameraUtils.decodeBitmap(picture, new CameraUtils.BitmapCallback() {
                    @Override
                    public void onBitmapReady(Bitmap bitmap) {
                        imageView.setImageBitmap(bitmap);
                        image = picture;

                    }
                });
            }
        });

        makePhotoButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                camera.capturePicture();
            }
        });

        sendImageButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                MyTask task = new MyTask(image);
                task.execute();
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();

        camera.start();
    }

    @Override
    protected void onPause() {
        super.onPause();
        camera.stop();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        camera.destroy();
    }


    class MyTask extends AsyncTask<Void, Void, Void> {
        Socket socket;
        byte[] image;
        MyTask(byte[] image){
            this.image = image;
        }
        OutputStream outputStream;
        @Override
        protected void onPreExecute() {
            super.onPreExecute();

        }

        @Override
        protected Void doInBackground(Void... params) {
            try {
                    String hostname = "192.168.103.175";
                    int port = 4000;

                    try {
                        socket = new Socket(hostname, port);
                        outputStream = socket.getOutputStream();

                        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();

                        byteArrayOutputStream.write(image);
                        // get the size of image
                        byte[] size = ByteBuffer.allocate(4).putInt(image.length).array();
                        outputStream.write(size);
                        outputStream.write(image);

                        outputStream.close();
                        socket.close();
                    } catch (Exception ex) {
                        Log.e("Error server ", ex.getMessage());
                    }

            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }



        @Override
        protected void onPostExecute(Void result) {
            super.onPostExecute(result);
        }
    }

}
