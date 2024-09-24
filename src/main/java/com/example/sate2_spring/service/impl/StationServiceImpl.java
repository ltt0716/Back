package com.example.sate2_spring.service.impl;

import com.example.sate2_spring.bean.GlobalStar.GlobalStar_TLE;
import com.example.sate2_spring.bean.GlobalStar.GlobalStar_six;
import com.example.sate2_spring.bean.Iridium.Iridium_TLE;
import com.example.sate2_spring.bean.Iridium.Iridium_six;
import com.example.sate2_spring.bean.Station;
import com.example.sate2_spring.bean.Telesat.Telesat_TLE;
import com.example.sate2_spring.bean.Telesat.Telesat_six;
import com.example.sate2_spring.mapper.StationMapper;
import com.example.sate2_spring.service.util.StationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class StationServiceImpl implements StationService {
    @Autowired
    private StationMapper stationMapper;
    @Override
    public int add(Station station) {
        return stationMapper.add(station);
    }
    @Override
    public List<Station> getAllBook() {

        List<Station> stations =stationMapper.getAllBook();
        return stations;
    }

    @Override
    public void delete(String id) {
        stationMapper.deleteBook(id);

    }

    @Override
    public void update(Station station) {
        stationMapper.update(station);
    }

    @Override
    public Station getById(String id) {
        Station station=stationMapper.getById(id);
        return station;
    }
//tle
    @Override
    public List<GlobalStar_TLE> GlobalStartles_getAll() {
        List<GlobalStar_TLE> tles =stationMapper.GlobalStartles_getAll();
        return tles;
    }

    @Override
    public int addtleGlobalStar(GlobalStar_TLE tle) {
        return stationMapper.addGlobalStartle(tle);
    }

    @Override
    public void deleteGlobalStar_TLE(String id) {
        stationMapper.deleteGlobalStar_TLE(id);
    }

    @Override
    public GlobalStar_TLE getByIdGlobalStar_TLE(String id) {

        GlobalStar_TLE tle=stationMapper.getByIdGlobalStar_TLE(id);
        return tle;
    }

    @Override
    public void updateGlobalStartle(GlobalStar_TLE tle) {
        stationMapper.updateGlobalStartle(tle);
    }

    //six
    @Override
    public List<GlobalStar_six> GlobalStarsixs_getAll() {
        List<GlobalStar_six> sixs =stationMapper.GlobalStarsixs_getAll();
        return sixs;
    }

    @Override
    public int addsixGlobalStar(GlobalStar_six six) {
        return stationMapper.addGlobalStarsix(six);
    }

    @Override
    public void deleteGlobalStar_six(String id) {
        stationMapper.deleteGlobalStar_six(id);
    }

    @Override
    public GlobalStar_six getByIdGlobalStar_six(String id) {

        GlobalStar_six six=stationMapper.getByIdGlobalStar_six(id);
        return six;
    }

    @Override
    public void updateGlobalStarsix(GlobalStar_six six) {
        stationMapper.updateGlobalStarsix(six);
    }


    //tle
    @Override
    public List<Iridium_TLE> Iridiumtles_getAll() {
        List<Iridium_TLE> tles =stationMapper.Iridiumtles_getAll();
        return tles;
    }

    @Override
    public int addtleIridium(Iridium_TLE tle) {
        return stationMapper.addIridiumtle(tle);
    }

    @Override
    public void deleteIridium_TLE(String id) {
        stationMapper.deleteIridium_TLE(id);
    }

    @Override
    public Iridium_TLE getByIdIridium_TLE(String id) {

        Iridium_TLE tle=stationMapper.getByIdIridium_TLE(id);
        return tle;
    }

    @Override
    public void updateIridiumtle(Iridium_TLE tle) {
        stationMapper.updateIridiumtle(tle);
    }

    //six
    @Override
    public List<Iridium_six> Iridiumsixs_getAll() {
        List<Iridium_six> sixs =stationMapper.Iridiumsixs_getAll();
        return sixs;
    }

    @Override
    public int addsixIridium(Iridium_six six) {
        return stationMapper.addIridiumsix(six);
    }

    @Override
    public void deleteIridium_six(String id) {
        stationMapper.deleteIridium_six(id);
    }

    @Override
    public Iridium_six getByIdIridium_six(String id) {

        Iridium_six six=stationMapper.getByIdIridium_six(id);
        return six;
    }

    @Override
    public void updateIridiumsix(Iridium_six six) {
        stationMapper.updateIridiumsix(six);
    }
    //tle
    @Override
    public List<Telesat_TLE> Telesattles_getAll() {
        List<Telesat_TLE> tles =stationMapper.Telesattles_getAll();
        return tles;
    }

    @Override
    public int addtleTelesat(Telesat_TLE tle) {
        return stationMapper.addTelesattle(tle);
    }

    @Override
    public void deleteTelesat_TLE(String id) {
        stationMapper.deleteTelesat_TLE(id);
    }

    @Override
    public Telesat_TLE getByIdTelesat_TLE(String id) {

        Telesat_TLE tle=stationMapper.getByIdTelesat_TLE(id);
        return tle;
    }

    @Override
    public void updateTelesattle(Telesat_TLE tle) {
        stationMapper.updateTelesattle(tle);
    }

    //six
    @Override
    public List<Telesat_six> Telesatsixs_getAll() {
        List<Telesat_six> sixs =stationMapper.Telesatsixs_getAll();
        return sixs;
    }

    @Override
    public int addsixTelesat(Telesat_six six) {
        return stationMapper.addTelesatsix(six);
    }

    @Override
    public void deleteTelesat_six(String id) {
        stationMapper.deleteTelesat_six(id);
    }

    @Override
    public Telesat_six getByIdTelesat_six(String id) {

        Telesat_six six=stationMapper.getByIdTelesat_six(id);
        return six;
    }

    @Override
    public void updateTelesatsix(Telesat_six six) {
        stationMapper.updateTelesatsix(six);
    }



}
