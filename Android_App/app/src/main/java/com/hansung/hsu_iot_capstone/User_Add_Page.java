package com.hansung.hsu_iot_capstone;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class User_Add_Page extends AppCompatActivity {
    private String admin_id;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.user_add_layout);
        //Intent intent = getIntent();
        //this.admin_id = intent.getStringExtra("admin_id");
        //System.out.println(admin_id);
        admin_id = "hsu_admin";
    }

    public void add_user_btn(View v) {
        EditText name = findViewById(R.id.editText_name);
        EditText age = findViewById(R.id.editText_age);
        EditText gender = findViewById(R.id.editText_gender);

        if (name.getText().toString().length() == 0) {
            Toast.makeText(this.getApplicationContext(), "아이디를 입력해주세요!", Toast.LENGTH_SHORT).show();
        } else if (age.getText().toString().length() == 0) {
            Toast.makeText(this.getApplicationContext(), "비밀번호를 입력해주세요!", Toast.LENGTH_SHORT).show();
        } else if (gender.getText().toString().length() == 0) {
            Toast.makeText(this.getApplicationContext(), "성별 정보를 입력해주세요!", Toast.LENGTH_SHORT).show();
        } else if (!gender.getText().toString().equals("man") && !gender.getText().toString().equals("woman")) {
            Toast.makeText(this.getApplicationContext(), "성별 정보를 man 혹은 woman으로 입력해주세요!", Toast.LENGTH_SHORT).show();
        } else {
            JSONObject jsonObject = new JSONObject();
            try {
                jsonObject.put("admin_id", admin_id.toString());
                jsonObject.put("id", name.getText().toString());
                jsonObject.put("age", age.getText().toString());
                jsonObject.put("gender", gender.getText().toString());
                jsonObject.put("status", "debug");
                jsonObject.put("interest", "debug");
                System.out.println(jsonObject.toString());
            } catch (JSONException e) {
                e.printStackTrace();
            }

            final String jsonInputString = jsonObject.toString();

            new Thread((new Runnable() {
                @Override
                public void run() {
                    try {
                        URL url = new URL("http://hiroshilin.iptime.org:20000/add_user");
                        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                        conn.setRequestMethod("POST");
                        conn.setRequestProperty("Content-Type", "application/json; utf-8");
                        conn.setRequestProperty("Accept", "application/json");
                        conn.setDoOutput(true);
                        conn.getOutputStream().write(jsonInputString.getBytes("utf-8"));

                        if (conn.getResponseCode() != 200) {
                            throw new RuntimeException("Failed : HTTP error code : " + conn.getResponseCode());
                        }
                        /*
                        InputStream inputStream = conn.getInputStream();
                        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream, "utf-8"));
                        StringBuilder stringBuilder = new StringBuilder();
                        String line;
                        while ((line = bufferedReader.readLine()) != null) {
                            stringBuilder.append(line);
                        }
                        inputStream.close();

                         */
                        conn.disconnect();
                        Intent intent = new Intent();
                        setResult(RESULT_OK, intent);
                        finish();

                    } catch (MalformedURLException e) {
                        throw new RuntimeException(e);
                    } catch (IOException e) {
                        throw new RuntimeException(e);
                    }
                }
            })).start();
        }
    }
}