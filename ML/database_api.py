import logging
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import time
import queue

app = Flask(__name__)
CORS(app) 


data_queue = queue.Queue()

logging.basicConfig(level=logging.DEBUG)

@app.route('/upload_blob', methods=['POST'])
def upload_blob():
    """
    Endpoint to handle blob file upload and save each frame with a unique filename in the queue.
    """
    app.logger.debug("Received POST request on /upload_blob")

    if 'video' not in request.files:
        app.logger.error("No video file in the request")
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    if not latitude or not longitude:
        app.logger.error("Missing latitude or longitude in the request")
        return jsonify({"error": "Missing latitude or longitude"}), 400

    timestamp = int(time.time() * 1000)  
    filename = secure_filename(f"{timestamp}_{video_file.filename}")

    # Read video file data
    video_data = video_file.read()
    
    # Create metadata
    metadata = {
        "latitude": latitude,
        "longitude": longitude,
        "filename": filename,
        "timestamp": timestamp
    }

    # Store both video data and metadata in the queue
    data_queue.put({"video": video_data, "metadata": metadata})
    app.logger.info(f"Data added to queue: filename={filename}, metadata={metadata}")

    return jsonify({"message": "Frame and metadata added to queue successfully"}), 200


@app.route('/process_queue', methods=['GET'])
def process_queue():
    """
    Endpoint to process the queue and retrieve the next item.
    """
    if data_queue.empty():
        app.logger.info("Queue is empty")
        return jsonify({"message": "No data to process"}), 200

    data_item = data_queue.get()
    app.logger.info(f"Processing data from queue: {data_item['metadata']}")
    return jsonify({
        "message": "Data processed",
        "metadata": data_item['metadata']
    }), 200


@app.after_request
def add_cors_headers(response):
    """
    Adds CORS headers to every response for frontend compatibility.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


if __name__ == '__main__':
    app.run(debug=True)
