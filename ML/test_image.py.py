import cv2
import tensorflow as tf
import numpy as np
from ultralytics import YOLO


ESRGAN_MODEL_PATH = './esrgan_model'
YOLO_MODEL_PATH = 'best.pt'

yolo_model = YOLO(YOLO_MODEL_PATH)
esrgan_model = tf.saved_model.load(ESRGAN_MODEL_PATH)


def preprocess_image(image):
    hr_image = tf.convert_to_tensor(image, dtype=tf.float32)
    hr_size = (tf.convert_to_tensor(hr_image.shape[:-1]) // 4) * 4
    hr_image = tf.image.crop_to_bounding_box(hr_image, 0, 0, hr_size[0], hr_size[1])
    return tf.expand_dims(hr_image, 0)
 
frame_path = '/Users/sushanthraj/Desktop/campus_data/WhatsApp Image 2024-08-20 at 18.05.09 (2).jpeg'

frame = cv2.imread(frame_path)

lr_image = preprocess_image(frame)
sr_image = esrgan_model(lr_image)
sr_image = tf.squeeze(sr_image).numpy().astype(np.uint8)

results = yolo_model.predict(sr_image)
pothole_detected = False

for r in results:
    if len(r.boxes) > 0:
        pothole_detected = True
        break

if pothole_detected:
    print('pothole found')