package com.example.sate2_spring.controller;
import com.example.sate2_spring.bean.GlobalStar.GlobalStar_TLE;
import com.example.sate2_spring.bean.GlobalStar.GlobalStar_six;
import com.example.sate2_spring.bean.Station;
import com.example.sate2_spring.service.util.StationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

@Controller
@RequestMapping("/GlobalStar")
public class GlobalStar {
    @Autowired
    private StationService stationService;

    @RequestMapping("/tle_getAll")
    public String getAll(Model model) {
        List<GlobalStar_TLE> tles=stationService.GlobalStartles_getAll();
        model.addAttribute("tles", tles);
//        System.out.println(tles);
        return "/Systems/GlobalStar/TLE/GlobalStar";
    }
    @RequestMapping("/tleAddPage")
    public String toAddPage() {
        return "/Systems/GlobalStar/TLE/GlobalStar_add";
    }

    @RequestMapping("/addtle")
    public String addtle(GlobalStar_TLE tle){

        if(stationService.addtleGlobalStar(tle)==1)
            return "redirect:/GlobalStar/tle_getAll";
        else
            return "null";
    }

    @RequestMapping("/deletetle/{id}")
    public String delete(@PathVariable("id") String id) {
        stationService.deleteGlobalStar_TLE(id);
        return "redirect:/GlobalStar/tle_getAll";
    }

    @RequestMapping("/toEditPagetle/{id}")
    public String toEditPagetle(Model model, @PathVariable("id") String id) {
        GlobalStar_TLE tle = stationService.getByIdGlobalStar_TLE(id);
        model.addAttribute("tle", tle);
        return "/Systems/GlobalStar/TLE/GlobalStar_edit";
    }
    @RequestMapping("/updateGlobalStartle/")
    public String updateGlobalStartle(GlobalStar_TLE tle) {
        stationService.updateGlobalStartle(tle);
        return "redirect:/GlobalStar/tle_getAll";
    }
    //six
    @RequestMapping("/six_getAll")
    public String getAllsix(Model model) {
        List<GlobalStar_six> sixs=stationService.GlobalStarsixs_getAll();
        model.addAttribute("sixs", sixs);
//        System.out.println(tles);
        return "/Systems/GlobalStar/six/GlobalStar";
    }
    @RequestMapping("/sixAddPage")
    public String toAddPagesix() {
        return "/Systems/GlobalStar/six/GlobalStar_add";
    }

    @RequestMapping("/addsix")
    public String addsix(GlobalStar_six six){

        if(stationService.addsixGlobalStar(six)==1)
            return "redirect:/GlobalStar/six_getAll";
        else
            return "null";
    }

    @RequestMapping("/deletesix/{id}")
    public String deletesix(@PathVariable("id") String id) {
        stationService.deleteGlobalStar_six(id);
        return "redirect:/GlobalStar/six_getAll";
    }

    @RequestMapping("/toEditPagesix/{id}")
    public String toEditPagesix(Model model, @PathVariable("id") String id) {
        GlobalStar_six six = stationService.getByIdGlobalStar_six(id);
        model.addAttribute("six", six);
        return "/Systems/GlobalStar/six/GlobalStar_edit";
    }
    @RequestMapping("/updateGlobalStarsix/")
    public String updateGlobalStarsix(GlobalStar_six six) {
        stationService.updateGlobalStarsix(six);
        return "redirect:/GlobalStar/six_getAll";
    }
}
