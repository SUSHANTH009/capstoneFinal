package com.example.potholeDetection.clustering;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor


@Entity
@Table(name = "Centroid")
public class Centroid {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;

    @Column(name="Longitude", nullable = false)
    private double centroidLongitude;

    @Column(name="Latitude", nullable = false)
    private double centroidLatitude;

    public Centroid(double centroidLatitude, double centroidLongitude) {
        this.centroidLatitude = centroidLatitude;
        this.centroidLongitude = centroidLongitude;
    }


}
