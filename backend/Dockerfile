# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI default port
EXPOSE 8000

# Run the app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

