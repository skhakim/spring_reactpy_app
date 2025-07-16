# Use official Python slim image for a smaller footprint
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy the application code
COPY name_lookup.py .

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Expose port 4000 for the ReactPy app
EXPOSE 4000

# Command to run the ReactPy application
CMD ["python", "name_lookup.py"]
