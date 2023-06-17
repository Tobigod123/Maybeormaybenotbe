# Use the official Python image as the base image

FROM python:3.9.7-slim-buster

# Set the working directory to /app

WORKDIR /app

# Copy the necessary files into the container

COPY . /app

# Install system dependencies

RUN apt-get update && apt-get install -y --no-install-recommends \

    ffmpeg \

    mediainfo \

    && rm -rf /var/lib/apt/lists/*

# Install project dependencies

RUN pip install --no-cache-dir --upgrade pip \

    && pip install --no-cache-dir -r requirements.txt

# Expose the necessary port(s) for the application (if applicable)

EXPOSE 5000

# Set the entrypoint command

CMD ["python3", "main.py"]
