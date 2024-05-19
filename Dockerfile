# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN chmod 777 /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

RUN mkdir -p /usr/src/app/shared

# Create a directory for NLTK data and set permissions
RUN mkdir -p /usr/local/nltk_data && chmod a+rwx /usr/local/nltk_data
  
RUN python -m nltk.downloader punkt -d /usr/local/nltk_data
# Switch to the non-privileged user to run the application.

# Copy the source code into the container.
COPY . .

ENV SHARED=/usr/src/app/shared

# Expose the port that the application listens on.
EXPOSE 5000

# Run the application.
CMD ["python", "app.py"]