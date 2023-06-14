package com.hansung.hsu_iot_capstone;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

public class Admin_manage_page extends AppCompatActivity {
    private static final int REQUEST_CODE_USER_ADD = 200;
    static ManageAdapter adapter;
    private ProgressDialog progressDialog;
    private String admin_id;
    private HttpURLConnection conn;
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.admin_manage_page);
        Intent intent = getIntent();
        this.admin_id = intent.getStringExtra("admin_id");
        ArrayList<Data> data = new ArrayList<Data>();
        getManageUserName(data);
        adapter = new ManageAdapter(this, R.layout.item_layout, data);

        ListView listView = (ListView)findViewById(R.id.listView);
        listView.setAdapter(adapter);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                String name = ((Data)adapter.getItem(i)).getName();
                Toast.makeText(Admin_manage_page.this, name + " selected", Toast.LENGTH_SHORT).show();
            }
        });
    }

    public void startUserAddPage() {
        Intent intent = new Intent(this, User_Add_Page.class);
        ((AppCompatActivity) this).startActivityForResult(intent, REQUEST_CODE_USER_ADD);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_CODE_USER_ADD && resultCode == RESULT_OK) {
            // Admin_manage_page를 재실행하고 데이터를 업데이트하는 로직을 여기에 작성합니다.
            restartAdminManagePage();
        }
    }

    private void restartAdminManagePage() {
        Intent intent = getIntent();
        finish();
        startActivity(intent);
    }



    private void getManageUserName(ArrayList<Data> data) {
        progressDialog = new ProgressDialog(Admin_manage_page.this);
        progressDialog.setMessage("로딩 중...");
        progressDialog.setCancelable(false);
        progressDialog.show();
        new Thread(new Runnable() {
            @Override
            public void run() {
                HttpURLConnection conn = null; // 변경된 부분
                HttpURLConnection conn_user = null; // 변경된 부분
                try {
                    URL url = new URL("http://hiroshilin.iptime.org:20000/get_admin_manage_user/" + admin_id);
                    conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("GET");
                    conn.setRequestProperty("Content-Type", "application/json; utf-8");
                    conn.setRequestProperty("Accept", "application/json");
                    if (conn.getResponseCode() != 200) {
                        throw new RuntimeException("Failed : HTTP error code : " + conn.getResponseCode());
                    }
                    InputStream inputStream = conn.getInputStream();
                    BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream, "utf-8"));
                    StringBuilder stringBuilder = new StringBuilder();
                    String line;
                    while ((line = bufferedReader.readLine()) != null) {
                        stringBuilder.append(line);
                    }
                    inputStream.close();

                    final String result = stringBuilder.toString();
                    final JSONArray jsonArray = new JSONArray(result);
                    final int length = jsonArray.length();
                    for (int i = 0; i < length; i++) {
                        String name = jsonArray.getString(i);
                        URL user_url = new URL("http://hiroshilin.iptime.org:20000/get_interest_user/" + name);
                        conn_user = (HttpURLConnection) user_url.openConnection();
                        conn_user.setRequestMethod("GET");
                        conn_user.setRequestProperty("Content-Type", "application/json; utf-8");
                        conn_user.setRequestProperty("Accept", "application/json");
                        if (conn_user.getResponseCode() != 200) {
                            throw new RuntimeException("Failed : HTTP error code : " + conn_user.getResponseCode());
                        }
                        InputStream user_input_stream = conn_user.getInputStream();
                        BufferedReader user_bufferedReader = new BufferedReader(new InputStreamReader(user_input_stream, "utf-8"));
                        StringBuilder user_stringBuilder = new StringBuilder();
                        String user_line;
                        while ((user_line = user_bufferedReader.readLine()) != null) {
                            user_stringBuilder.append(user_line);
                        }
                        user_input_stream.close();

                        String user_result = user_stringBuilder.toString();
                        JSONArray user_jsonarray = new JSONArray(user_result);
                        StringBuilder statusBuilder = new StringBuilder();
                        int user_length = user_jsonarray.length();
                        for (int j = 0; j < user_length; j++) {
                            switch (j) {
                                case 0:
                                    statusBuilder.append("기타 : ").append(user_jsonarray.getInt(j));
                                    break;
                                case 1:
                                    statusBuilder.append(" 요리 : ").append(user_jsonarray.getInt(j));
                                    break;
                                case 2:
                                    statusBuilder.append(" 바둑 : ").append(user_jsonarray.getInt(j));
                                    break;
                                case 3:
                                    statusBuilder.append(" 미술 : ").append(user_jsonarray.getInt(j));
                                    break;
                                case 4:
                                    statusBuilder.append(" 운동 : ").append(user_jsonarray.getInt(j));
                                    break;
                                case 5:
                                    statusBuilder.append(" 영화 : ").append(user_jsonarray.getInt(j));
                                    break;
                                case 6:
                                    statusBuilder.append(" 건강 : ").append(user_jsonarray.getInt(j));
                                    break;
                                case 7:
                                    statusBuilder.append(" 교양 : ").append(user_jsonarray.getInt(j));
                                    break;
                                case 8:
                                    statusBuilder.append(" 상담 : ").append(user_jsonarray.getInt(j));
                                    String updatedStatus = statusBuilder.toString();
                                    data.add(new Data(R.drawable.ic_launcher_foreground, name, updatedStatus));
                                    break;
                            }
                        }
                    }
                } catch (MalformedURLException e) {
                    throw new RuntimeException(e);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                } catch (JSONException e) {
                    throw new RuntimeException(e);
                } finally {
                    if (conn != null) {
                        conn.disconnect();
                    }
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            progressDialog.dismiss();
                        }
                    });
                }
            }
        }).start();
    }

}

//https://kadosholy.tistory.com/53