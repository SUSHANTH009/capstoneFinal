package com.example.potholeDetection.geodata;

// import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;
import org.springframework.data.jpa.repository.JpaRepository;


@Repository
public interface LocationRepository extends JpaRepository<Location, Long>{

    Location findByLatitudeAndLongitude(double latitude, double longitude);
}