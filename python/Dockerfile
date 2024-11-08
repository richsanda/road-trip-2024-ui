# Use the Python 3.9 slim base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the source code and required files to the container
COPY ./src /app/src
COPY connection.py /app/
COPY server.py /app/
COPY database.db /app/
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080
EXPOSE 8080

# Command to run the Flask server
CMD ["python", "server.py"]
