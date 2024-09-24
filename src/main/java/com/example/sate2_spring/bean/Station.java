package com.example.sate2_spring.bean;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;


@Data
public class Station {
    private String id;
    private String name;
    private String description;
    private Double position_x;
    private Double position_y;
    private Double position_z;



}
