package com.example.potholeDetection.distance;

import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.potholeDetection.geodata.Location;

@RestController
@RequestMapping("/api/distance")
public class DistanceController {

   DistanceService distanceService;

    public DistanceController(DistanceService distanceService) {
        this.distanceService = distanceService;
    }

    @PostMapping("/live")
    public ResponseEntity<Map<String, String>> alert(@RequestBody Location location) {
         return distanceService.calculate(location);
    }
}
