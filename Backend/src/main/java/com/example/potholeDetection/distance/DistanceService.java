package com.example.potholeDetection.distance;

import java.util.List;

import org.springframework.stereotype.Service;

import com.example.potholeDetection.geodata.Location;
import com.example.potholeDetection.geodata.LocationRepository;

@Service
public class DistanceService {

    DistanceCalculatorService distanceCalculatorService;
    LocationRepository locationRepository;


    public DistanceService(DistanceCalculatorService distanceCalculatorService,LocationRepository locationRepository) {
        this.distanceCalculatorService = distanceCalculatorService;
        this.locationRepository = locationRepository;
    }

    


    public String calculate(Location source) {
        List<Location> allLocations = locationRepository.findAll();
        final int BATCH_SIZE = 25;
        String response = "No Pothole Ahead.";
    
        for (int i = 0; i < allLocations.size(); i += BATCH_SIZE) {
            int end = Math.min(i + BATCH_SIZE, allLocations.size());
            List<Location> batch = allLocations.subList(i, end);
            try {
                String batchResponse = distanceCalculatorService.getData(source, batch);
                if (batchResponse=="Pothole Ahead") {
                    return batchResponse; // Immediately return if a pothole is detected in any batch
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    
        return response; // Return "No Pothole Ahead." if no batches detect a pothole
    }
    
}
