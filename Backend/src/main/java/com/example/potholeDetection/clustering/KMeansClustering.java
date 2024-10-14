package com.example.potholeDetection.clustering;

import weka.clusterers.SimpleKMeans;
import weka.core.Instances;
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Component;

import com.example.potholeDetection.geodata.Location;

import weka.core.Attribute;
import weka.core.DenseInstance;
import weka.core.Instance;

@Component
public class KMeansClustering {

    public List<Centroid> findCentroids(List<Location> locations, int numClusters) throws Exception {
        Instances data = createInstancesFromLocations(locations);

        SimpleKMeans kMeans = new SimpleKMeans();
        kMeans.setNumClusters(numClusters);
        kMeans.buildClusterer(data);

        List<Centroid> centroids = new ArrayList<>();
        int actualClusters = kMeans.numberOfClusters(); // Get the actual number of clusters found
    for (int i = 0; i < actualClusters; i++) {
            Instance centroid = kMeans.getClusterCentroids().instance(i);
            Centroid centroidLocation = new Centroid();
            centroidLocation.setCentroidLongitude(centroid.value(0));
            centroidLocation.setCentroidLatitude(centroid.value(1));
            centroids.add(centroidLocation);
        }
        return centroids;   
    }

    private Instances createInstancesFromLocations(List<Location> locations) {
        ArrayList<Attribute> attributes = new ArrayList<>();
        attributes.add(new Attribute("longitude"));
        attributes.add(new Attribute("latitude"));

        Instances instances = new Instances("LocationInstances", attributes, locations.size());

        for (Location loc : locations) {
            double[] values = new double[2];
            values[0] = loc.getLongitude();
            values[1] = loc.getLatitude();
            instances.add(new DenseInstance(1.0, values));
        }

        return instances;
    }
}
