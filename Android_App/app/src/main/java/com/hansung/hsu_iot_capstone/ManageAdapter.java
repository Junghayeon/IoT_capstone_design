package com.hansung.hsu_iot_capstone;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

public class ManageAdapter extends BaseAdapter {
    private static final int VIEW_TYPE_NORMAL = 0;
    private static final int VIEW_TYPE_ADD = 1;
    private Context mContext;
    private int mResource;
    private ArrayList<Data> data = new ArrayList<Data>();

    public ManageAdapter(Context context, int resource, ArrayList<Data> datas) {
        this.mContext = context;
        this.data = datas;
        this.mResource = resource;
    }
    @Override
    public int getCount() {
        return data.size() + 1;
    }

    @Override
    public Object getItem(int i) {
        if(i < data.size())
            return data.get(i);
        else {
            return null;
        }
    }

    @Override
    public int getItemViewType(int i) {
        if(i < data.size())
            return VIEW_TYPE_NORMAL;
        else
            return VIEW_TYPE_ADD;
    }

    @Override
    public int getViewTypeCount() {
        return 2; //VIEW_TYPE_NORMAL, VIEW_TYPE_ADD
    }

    @Override
    public long getItemId(int i) {
        return i;
    }

    @Override
    public View getView(int i, View view, ViewGroup viewGroup) {
        ViewHolder viewHolder;
        int viewType = getItemViewType(i);
        if(view == null) {
            viewHolder = new ViewHolder();
            LayoutInflater inflater= (LayoutInflater)mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);

            if(viewType == VIEW_TYPE_NORMAL) {
                view = inflater.inflate(mResource, viewGroup, false);
                viewHolder.icon = view.findViewById(R.id.image_view);
                viewHolder.name = view.findViewById(R.id.text_name);
                viewHolder.status = view.findViewById(R.id.text_status);
            } else {
                view = inflater.inflate(R.layout.list_item_add, viewGroup, false);
                viewHolder.addButton = view.findViewById(R.id.add_button);
            }
            view.setTag(viewHolder);
            //view = inflater.inflate(mResource, viewGroup, false);
        } else {
            viewHolder = (ViewHolder) view.getTag();
        }

        if(viewType == VIEW_TYPE_NORMAL) {
            Data item = data.get(i);
            viewHolder.icon = view.findViewById(R.id.image_view);
            viewHolder.icon.setImageResource(item.mIcon);
            viewHolder.name.setText(item.getName());
            viewHolder.status.setText(item.getStatus());
        } else {
            viewHolder.addButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    Toast.makeText(mContext, "ADD BTN Click", Toast.LENGTH_SHORT).show();
                    if (mContext instanceof Admin_manage_page) {
                        ((Admin_manage_page) mContext).startUserAddPage();
                    }
                    //Intent intent = new Intent(mContext, User_Add_Page.class);
                    //mContext.startActivity(intent);
                }
            });
        }

        /*
        ImageView icon = view.findViewById(R.id.image_view);
        icon.setImageResource(data.get(i).mIcon);
        TextView name = view.findViewById(R.id.text_name);
        name.setText(data.get(i).getName());

        TextView status = view.findViewById(R.id.text_status);
        status.setText(data.get(i).getStatus());
         */

        return view;
    }

    private static class ViewHolder {
        ImageView icon;
        TextView name;
        TextView status;
        Button addButton;
    }
}
