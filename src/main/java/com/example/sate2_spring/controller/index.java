package com.example.sate2_spring.controller;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.example.sate2_spring.bean.Station;

@Controller
public class index{
//
//    @RequestMapping("/")
//    public String login(){
//        return "index";
//    }


    @RequestMapping("/interval")
    public String To_Interval(){
        return "interval";
    }
    @RequestMapping("/RealTime")
    public String To_RealTime(){
        return "RealTime";
    }

    @RequestMapping("/c")
    public String loginc(){
//        return "interval";
        return "info";
    }

    @RequestMapping("/d")
    public String logind(){
//        return "interval";
        return "aa";
    }





}
