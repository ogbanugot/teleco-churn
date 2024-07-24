# First Stage: Base Image with Python
FROM python:3.8 AS base

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wget \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Second Stage: Slim Python Image
FROM python:3.9-slim AS final

# Set working directory
WORKDIR /app

# Copy from base image
COPY --from=base /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/

# Install additional system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY ./ /app

# Download the model file
RUN wget https://github.com/download/v0.1.0/best.pt

# Expose port
EXPOSE 8080