FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl unzip gnupg wget libnss3 libatk-bridge2.0-0 libxss1 libasound2 libgtk-3-0 \
    libgbm1 libxshmfence1 libxcomposite1 libxdamage1 libxrandr2 libgl1 libglu1-mesa xvfb \
    && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir flask playwright

# Install Chromium for Playwright
RUN playwright install chromium

# Set working directory
WORKDIR /app

# Copy code into container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Start Flask server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
