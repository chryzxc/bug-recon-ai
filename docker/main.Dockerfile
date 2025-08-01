FROM python:3.9-slim

WORKDIR /app

# Install core dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app /app

# Use ENTRYPOINT for executable, CMD for default arguments
ENTRYPOINT ["python", "main.py"]
CMD ["example.com"]  # Default target if none provided