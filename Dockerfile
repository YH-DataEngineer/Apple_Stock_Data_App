FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .


# Expose port 8000
EXPOSE 8000

# Run the application - FIXED: must bind to 0.0.0.0 for Docker
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


#docker build -t aapl-stock-api .
#docker run -p 8000:8000 aapl-stock-api