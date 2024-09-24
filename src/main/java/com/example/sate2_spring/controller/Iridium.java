package com.example.sate2_spring.controller;
import com.example.sate2_spring.bean.Iridium.Iridium_TLE;
import com.example.sate2_spring.bean.Iridium.Iridium_six;
import com.example.sate2_spring.bean.Station;
import com.example.sate2_spring.service.util.StationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

@Controller
@RequestMapping("/Iridium")
public class Iridium {
    @Autowired
    private StationService stationService;

    @RequestMapping("/tle_getAll")
    public String getAll(Model model) {
        List<Iridium_TLE> tles=stationService.Iridiumtles_getAll();
        model.addAttribute("tles", tles);
//        System.out.println(tles);
        return "/Systems/Iridium/TLE/Iridium";
    }
    @RequestMapping("/tleAddPage")
    public String toAddPage() {
        return "/Systems/Iridium/TLE/Iridium_add";
    }

    @RequestMapping("/addtle")
    public String addtle(Iridium_TLE tle){

        if(stationService.addtleIridium(tle)==1)
            return "redirect:/Iridium/tle_getAll";
        else
            return "null";
    }

    @RequestMapping("/deletetle/{id}")
    public String delete(@PathVariable("id") String id) {
        stationService.deleteIridium_TLE(id);
        return "redirect:/Iridium/tle_getAll";
    }

    @RequestMapping("/toEditPagetle/{id}")
    public String toEditPagetle(Model model, @PathVariable("id") String id) {
        Iridium_TLE tle = stationService.getByIdIridium_TLE(id);
        model.addAttribute("tle", tle);
        return "/Systems/Iridium/TLE/Iridium_edit";
    }
    @RequestMapping("/updateIridiumtle/")
    public String updateIridiumtle(Iridium_TLE tle) {
        stationService.updateIridiumtle(tle);
        return "redirect:/Iridium/tle_getAll";
    }
    //six
    @RequestMapping("/six_getAll")
    public String getAllsix(Model model) {
        List<Iridium_six> sixs=stationService.Iridiumsixs_getAll();
        model.addAttribute("sixs", sixs);
//        System.out.println(tles);
        return "/Systems/Iridium/six/Iridium";
    }
    @RequestMapping("/sixAddPage")
    public String toAddPagesix() {
        return "/Systems/Iridium/six/Iridium_add";
    }

    @RequestMapping("/addsix")
    public String addsix(Iridium_six six){

        if(stationService.addsixIridium(six)==1)
            return "redirect:/Iridium/six_getAll";
        else
            return "null";
    }

    @RequestMapping("/deletesix/{id}")
    public String deletesix(@PathVariable("id") String id) {
        stationService.deleteIridium_six(id);
        return "redirect:/Iridium/six_getAll";
    }

    @RequestMapping("/toEditPagesix/{id}")
    public String toEditPagesix(Model model, @PathVariable("id") String id) {
        Iridium_six six = stationService.getByIdIridium_six(id);
        model.addAttribute("six", six);
        return "/Systems/Iridium/six/Iridium_edit";
    }
    @RequestMapping("/updateIridiumsix/")
    public String updateIridiumsix(Iridium_six six) {
        stationService.updateIridiumsix(six);
        return "redirect:/Iridium/six_getAll";
    }
}
