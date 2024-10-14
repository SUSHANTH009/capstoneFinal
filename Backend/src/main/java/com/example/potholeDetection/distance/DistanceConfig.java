package com.example.potholeDetection.distance;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DistanceConfig {

    @Value("${api.key}")
    private String API_KEY;


    public String getAPI_KEY() {
        return API_KEY;
    }
}
