import os
import cv2
import sqlite3
import logging
import tensorflow as tf
import numpy as np
from ultralytics import YOLO
import requests

DB_PATH = 'frames_and_locations.db'
POTHOLE_DB_PATH = 'potholes_db.db' 
ESRGAN_MODEL_PATH = './esrgan_model'
YOLO_MODEL_PATH = 'best.pt'

yolo_model = YOLO(YOLO_MODEL_PATH)
esrgan_model = tf.saved_model.load(ESRGAN_MODEL_PATH)

logging.basicConfig(filename='pipeline.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

pothole_conn = sqlite3.connect(POTHOLE_DB_PATH)
pothole_cursor = pothole_conn.cursor()


def preprocess_image(image):
    hr_image = tf.convert_to_tensor(image, dtype=tf.float32)
    hr_size = (tf.convert_to_tensor(hr_image.shape[:-1]) // 4) * 4
    hr_image = tf.image.crop_to_bounding_box(hr_image, 0, 0, hr_size[0], hr_size[1])
    return tf.expand_dims(hr_image, 0)

cursor.execute("SELECT frame_id, frame_number, frame_path, latitude, longitude FROM frame_data")
frames = cursor.fetchall()

for frame_data in frames:
    frame_id, frame_number, frame_path, latitude, longitude = frame_data
    
    frame = cv2.imread(frame_path)
    if frame is None:
        logging.error(f"Error loading frame {frame_number} from {frame_path}. Skipping.")
        continue
    
    try:
        lr_image = preprocess_image(frame)
        sr_image = esrgan_model(lr_image)
        sr_image = tf.squeeze(sr_image).numpy().astype(np.uint8)
        logging.info(f"Frame {frame_number} enhanced using ESRGAN.")

    except Exception as e:
        logging.error(f"Error enhancing frame {frame_number}: {str(e)}")
        continue

    try:
        results = yolo_model.predict(sr_image)
        pothole_detected = False
        
        for r in results:
            if len(r.boxes) > 0:
                pothole_detected = True
                break

        if pothole_detected:

            pothole_cursor.execute('''
                INSERT INTO pothole_data (frame_number, latitude, longitude)
                VALUES (?, ?, ?)
            ''', (frame_number, latitude, longitude))
            pothole_conn.commit()

            url = "http://localhost:8080/api/location/"

            data = {
                "latitude": latitude,
                "longitude": longitude 
            }
            response = requests.post(url, json=data)

            logging.info(f"Pothole detected in frame {frame_number}, GPS location saved.")
        
        else:
            os.remove(frame_path)
            
        cursor.execute('DELETE FROM frame_data WHERE frame_id = ?', (frame_id,))
        conn.commit()

        logging.info(f"Frame {frame_number} processed and deleted from database.")

    except Exception as e:
        logging.error(f"Error during YOLOv9 detection for frame {frame_number}: {str(e)}")

conn.close()
pothole_conn.close()
logging.info("Pipeline processing complete.")