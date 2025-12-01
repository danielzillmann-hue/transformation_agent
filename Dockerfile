FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (minimal for now)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment
ENV PORT=8080

# Expose port (useful for local Docker runs; Cloud Run ignores EXPOSE)
EXPOSE 8080

# Start FastAPI app with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
