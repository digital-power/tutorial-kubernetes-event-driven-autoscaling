# Base python image
FROM python:3.9-slim

# Set working directory to /app
WORKDIR /app

# Copy requirements to working directory and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy src folder
COPY src/process_csv.py ./src/process_csv.py

# Run command on startup
ENTRYPOINT ["python", "src/process_csv.py"]