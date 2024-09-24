package com.example.sate2_spring.controller;

public class ReturnTime {

    private String Start_time;
    private String Stop_time;
    private String Current_time;

    public ReturnTime(String Start_time, String Stop_time,String Current_time) {
        this.Start_time = Start_time;
        this.Stop_time = Stop_time;
        this.Current_time=Current_time;
    }

    public String getStart_time() {return this.Start_time;}

    public String getStop_time()
    {
        return this.Stop_time;
    }

    public String getCurrent_time(){return Current_time;}

}
