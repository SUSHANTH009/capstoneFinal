import sqlite3
import cv2
import os
import random

db_path = 'frames_and_locations.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS frame_data (
    frame_id INTEGER PRIMARY KEY AUTOINCREMENT,
    frame_number INTEGER,
    frame_path TEXT,
    latitude REAL,
    longitude REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

video_path = 'potholes_video.mp4'  
frames_dir = 'frames'  
os.makedirs(frames_dir, exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def generate_random_gps():
    lat_range = (12.90, 13.00)
    lon_range = (77.55, 77.65)
    latitude = round(random.uniform(*lat_range), 6)
    longitude = round(random.uniform(*lon_range), 6)
    return latitude, longitude

cap = cv2.VideoCapture(video_path)
frame_number = 0

while cap.isOpened():
    ret, frame = cap.read()
    if ret:

        latitude, longitude = generate_random_gps()

        frame_filename = f"frame_{frame_number}.jpg"
        frame_path = os.path.join(frames_dir, frame_filename)
        cv2.imwrite(frame_path, frame)

        cursor.execute('''
            INSERT INTO frame_data (frame_number, frame_path, latitude, longitude)
            VALUES (?, ?, ?, ?)
        ''', (frame_number, frame_path, latitude, longitude))
        conn.commit()
        
        frame_number += 1
    else:
        break

# Release resources
cap.release()
conn.close()

print("Frame data and GPS locations stored successfully.")