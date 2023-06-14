package com.hansung.hsu_iot_capstone;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void login_btn(View v) {
        EditText admin_id = (EditText)findViewById(R.id.editText_id);
        EditText admin_pw = (EditText)findViewById(R.id.editText_password);
        if(admin_id.getText().toString().length() == 0) {
            Toast.makeText(this.getApplicationContext(), "아이디를 입력해주세요!", Toast.LENGTH_SHORT).show();
        } else if(admin_pw.getText().toString().length() == 0) {
            Toast.makeText(this.getApplicationContext(), "비밀번호를 입력해주세요!", Toast.LENGTH_SHORT).show();
        }
        new Thread((new Runnable() {
            @Override
            public void run() {
                try {
                    URL url = new URL("http://hiroshilin.iptime.org:20000/get_admin_pw/" + admin_id.getText().toString());
                    HttpURLConnection conn = (HttpURLConnection)url.openConnection();
                    conn.setRequestMethod("GET");
                    conn.setRequestProperty("Content-Type", "application/json; utf-8");
                    conn.setRequestProperty("Accept", "application/json");
                    if(conn.getResponseCode() != 200) {
                        throw new RuntimeException("Failed : HTTP error code : " + conn.getResponseCode());
                    }
                    InputStream inputStream = conn.getInputStream();
                    BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream, "utf-8"));
                    StringBuilder stringBuilder = new StringBuilder();
                    String line;
                    while((line = bufferedReader.readLine()) != null) {
                        stringBuilder.append(line);
                    }
                    System.out.println(line);
                    inputStream.close();
                    conn.disconnect();

                    final String result = stringBuilder.toString();
                    JSONObject jsonObject = new JSONObject(result);
                    final String pw = jsonObject.getString("pw");
                    if(admin_pw.getText().toString().equals(pw)) {
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                Toast.makeText(MainActivity.this, "login success!!!", Toast.LENGTH_SHORT).show();
                                Intent intent = new Intent(MainActivity.this, Admin_manage_page.class);
                                intent.putExtra("admin_id", admin_id.getText().toString());
                                startActivity(intent);
                            }
                        });
                    }
                } catch (MalformedURLException e) {
                    throw new RuntimeException(e);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                } catch (JSONException e) {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(MainActivity.this, "아이디나 패스워드가 틀립니다.", Toast.LENGTH_SHORT).show();
                        }
                    });
                    throw new RuntimeException(e);
                }
            }
        })).start();
    }
}