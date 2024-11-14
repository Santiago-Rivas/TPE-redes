# Use a basic Python image
FROM python:3.9-slim

# Install the required libraries
RUN pip install requests prometheus_client

# Copy the Python script into the container
COPY mailhog_exporter.py /usr/local/bin/mailhog_exporter.py

# Command to run the Python exporter
CMD ["python", "/usr/local/bin/mailhog_exporter.py"]
