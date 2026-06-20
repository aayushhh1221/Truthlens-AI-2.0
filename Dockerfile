# ─────────────────────────────────────────────
# TruthLens AI 2.0 — Dockerfile
# ─────────────────────────────────────────────
FROM python:3.11-slim

# System dependencies: tesseract for OCR, build tools for scipy/torch wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libtesseract-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create writable directory for the SQLite database
RUN mkdir -p /app/data
ENV DATABASE_PATH=/app/data/truthlens.db

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", \
            "--server.port=8501", \
            "--server.address=0.0.0.0", \
            "--server.headless=true"]
