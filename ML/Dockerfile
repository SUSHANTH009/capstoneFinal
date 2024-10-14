# Use a Python base image with TensorFlow support
FROM tensorflow/tensorflow:2.9.1-gpu

# Set working directory
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    python3-pip \
    libgl1-mesa-glx \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port for future use if needed
EXPOSE 8080

# Define entrypoint to run the pipeline script
ENTRYPOINT ["python3", "pipeline.py"]

RUN pip install flask