# Use the official Airflow image as the base image
FROM apache/airflow:latest-python3.11

# Switch to the root user temporarily to install additional packages
USER root

# Install wget and other packages
RUN apt-get update && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages for Airflow
USER airflow
RUN pip install --no-cache-dir biopython matplotlib xlsxwriter openpyxl
