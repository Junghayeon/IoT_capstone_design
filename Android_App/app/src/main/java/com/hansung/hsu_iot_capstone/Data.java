package com.hansung.hsu_iot_capstone;

public class Data {
    int mIcon;
    private String name;
    private String status;
    public Data(int mIcon, String name, String status) {
        this.mIcon = mIcon;
        this.name = name;
        this.status = status;
    }

    public String getName() {
        return name;
    }

    public String getStatus() {
        return status;
    }
}
