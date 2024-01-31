# Use the official Airflow image as the base image
FROM apache/airflow:latest-python3.11

# Switch to the root user temporarily to install additional packages
USER root

# Install wget
RUN apt-get update && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/*

# Switch back to the airflow user
USER airflow
