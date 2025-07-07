FROM python:3.12-slim

# Set working directory inside container to /backend
WORKDIR /backend

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    build-essential \           
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements file first (for dependency caching)
COPY requirements.txt .

# Install dependencies (this layer will be cached if requirements.txt doesn't change)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app from /backend/app/main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
