FROM python:3.10-slim-bullseye

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev python3-dev && \
    pip install --no-cache-dir --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt

# Copy application code
COPY . /app

# ✅ Add MongoDB environment variables
ENV MONGODB_VIDEOS_URI=mongodb://video-db:27017/videos
ENV MONGODB_USERS_URI=mongodb://user-db:27017/users

# Expose app port
EXPOSE 8080

# Run the Flask app
CMD ["python", "server.py"]
