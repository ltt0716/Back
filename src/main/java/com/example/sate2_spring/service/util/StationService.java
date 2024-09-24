package com.example.sate2_spring.service.util;

import com.example.sate2_spring.bean.GlobalStar.GlobalStar_TLE;
import com.example.sate2_spring.bean.GlobalStar.GlobalStar_six;
import com.example.sate2_spring.bean.Iridium.Iridium_TLE;
import com.example.sate2_spring.bean.Iridium.Iridium_six;
import com.example.sate2_spring.bean.Station;
import com.example.sate2_spring.bean.Telesat.Telesat_TLE;
import com.example.sate2_spring.bean.Telesat.Telesat_six;

import java.util.List;

public interface StationService {
    int add(Station station);

    List<Station> getAllBook();

    void delete(String id);

    void update(Station station);

    Station getById(String id);
    //tle
    List<GlobalStar_TLE> GlobalStartles_getAll();

    int addtleGlobalStar(GlobalStar_TLE tle);

    void deleteGlobalStar_TLE(String id);

    GlobalStar_TLE getByIdGlobalStar_TLE(String id);

    void updateGlobalStartle(GlobalStar_TLE tle);

    //six
    List<GlobalStar_six> GlobalStarsixs_getAll();

    int addsixGlobalStar(GlobalStar_six six);

    void deleteGlobalStar_six(String id);

    GlobalStar_six getByIdGlobalStar_six(String id);

    void updateGlobalStarsix(GlobalStar_six six);

    //tle
    List<Iridium_TLE> Iridiumtles_getAll();

    int addtleIridium(Iridium_TLE tle);

    void deleteIridium_TLE(String id);

    Iridium_TLE getByIdIridium_TLE(String id);

    void updateIridiumtle(Iridium_TLE tle);

    //six
    List<Iridium_six> Iridiumsixs_getAll();

    int addsixIridium(Iridium_six six);

    void deleteIridium_six(String id);

    Iridium_six getByIdIridium_six(String id);

    void updateIridiumsix(Iridium_six six);
    //tle
    List<Telesat_TLE> Telesattles_getAll();

    int addtleTelesat(Telesat_TLE tle);

    void deleteTelesat_TLE(String id);

    Telesat_TLE getByIdTelesat_TLE(String id);

    void updateTelesattle(Telesat_TLE tle);

    //six
    List<Telesat_six> Telesatsixs_getAll();

    int addsixTelesat(Telesat_six six);

    void deleteTelesat_six(String id);

    Telesat_six getByIdTelesat_six(String id);

    void updateTelesatsix(Telesat_six six);
}
