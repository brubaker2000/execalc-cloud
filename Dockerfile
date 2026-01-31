FROM python:3.11-slim

WORKDIR /app

# Install system deps for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy and install Python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . /app

ENV PYTHONPATH=/app
ENV PORT=8080

# Cloud Run expects the app to listen on $PORT
CMD ["sh","-c","gunicorn -b 0.0.0.0:${PORT} src.service.api:app"]
