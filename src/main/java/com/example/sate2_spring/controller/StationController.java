package com.example.sate2_spring.controller;

import com.example.sate2_spring.bean.Station;
import com.example.sate2_spring.service.util.StationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import java.util.List;


@Controller
@RequestMapping("/Station")
public class StationController {
    @Autowired
    private StationService stationService;

    @RequestMapping("/add")
    public String addSattion(Station station){

        if(stationService.add(station)==1)
            return "redirect:/Station/getAll";
        else
            return "null";
    }
    @RequestMapping("/getAll")
    public String getAll(Model model) {
        List<Station> stations = stationService.getAllBook();
        model.addAttribute("stations", stations);
        System.out.println(stations);
        return "/Station/station";
    }
    @RequestMapping("/toAddPage")
    public String toAddPage() {
        return "/Station/station_add";
    }



    @RequestMapping("/delete/{id}")
    public String delete(@PathVariable("id") String id) {
        stationService.delete(id);
        return "redirect:/Station/getAll";
    }
    @RequestMapping("/update")
    public String update(Station station) {
        stationService.update(station);
        return "redirect:/Station/getAll";
    }
    @RequestMapping("/toEditPage/{id}")
    public String toEditPage(Model model, @PathVariable("id") String id) {
        Station station = stationService.getById(id);
        model.addAttribute("station", station);
        return "/Station/station_edit";
    }

}
