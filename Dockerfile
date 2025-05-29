# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install make and other build dependencies
RUN apt-get update && apt-get install -y \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN make install

# Copy the rest of the application
COPY . .

# Run tests and linting
RUN make test lint

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 