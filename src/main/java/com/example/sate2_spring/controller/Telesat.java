package com.example.sate2_spring.controller;
import com.example.sate2_spring.bean.Telesat.Telesat_TLE;
import com.example.sate2_spring.bean.Telesat.Telesat_six;
import com.example.sate2_spring.bean.Station;
import com.example.sate2_spring.service.util.StationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

@Controller
@RequestMapping("/Telesat")
public class Telesat {
    @Autowired
    private StationService stationService;

    @RequestMapping("/tle_getAll")
    public String getAll(Model model) {
        List<Telesat_TLE> tles=stationService.Telesattles_getAll();
        model.addAttribute("tles", tles);
//        System.out.println(tles);
        return "/Systems/Telesat/TLE/Telesat";
    }
    @RequestMapping("/tleAddPage")
    public String toAddPage() {
        return "/Systems/Telesat/TLE/Telesat_add";
    }

    @RequestMapping("/addtle")
    public String addtle(Telesat_TLE tle){

        if(stationService.addtleTelesat(tle)==1)
            return "redirect:/Telesat/tle_getAll";
        else
            return "null";
    }

    @RequestMapping("/deletetle/{id}")
    public String delete(@PathVariable("id") String id) {
        stationService.deleteTelesat_TLE(id);
        return "redirect:/Telesat/tle_getAll";
    }

    @RequestMapping("/toEditPagetle/{id}")
    public String toEditPagetle(Model model, @PathVariable("id") String id) {
        Telesat_TLE tle = stationService.getByIdTelesat_TLE(id);
        model.addAttribute("tle", tle);
        return "/Systems/Telesat/TLE/Telesat_edit";
    }
    @RequestMapping("/updateTelesattle/")
    public String updateTelesattle(Telesat_TLE tle) {
        stationService.updateTelesattle(tle);
        return "redirect:/Telesat/tle_getAll";
    }
    //six
    @RequestMapping("/six_getAll")
    public String getAllsix(Model model) {
        List<Telesat_six> sixs=stationService.Telesatsixs_getAll();
        model.addAttribute("sixs", sixs);
//        System.out.println(tles);
        return "/Systems/Telesat/six/Telesat";
    }
    @RequestMapping("/sixAddPage")
    public String toAddPagesix() {
        return "/Systems/Telesat/six/Telesat_add";
    }

    @RequestMapping("/addsix")
    public String addsix(Telesat_six six){

        if(stationService.addsixTelesat(six)==1)
            return "redirect:/Telesat/six_getAll";
        else
            return "null";
    }

    @RequestMapping("/deletesix/{id}")
    public String deletesix(@PathVariable("id") String id) {
        stationService.deleteTelesat_six(id);
        return "redirect:/Telesat/six_getAll";
    }

    @RequestMapping("/toEditPagesix/{id}")
    public String toEditPagesix(Model model, @PathVariable("id") String id) {
        Telesat_six six = stationService.getByIdTelesat_six(id);
        model.addAttribute("six", six);
        return "/Systems/Telesat/six/Telesat_edit";
    }
    @RequestMapping("/updateTelesatsix/")
    public String updateTelesatsix(Telesat_six six) {
        stationService.updateTelesatsix(six);
        return "redirect:/Telesat/six_getAll";
    }
}
