FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive
ENV EXIFTOOL_PATH=/usr/bin/exiftool
ENV FFMPEG_PATH=/usr/bin/ffmpeg

# Install runtime dependencies (ffmpeg, exiftool) for media conversion
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    exiftool \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy repository content
COPY . /app

# Install dependencies and local packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080
EXPOSE 8080

# Launch FastAPI using shell form to support $PORT
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}