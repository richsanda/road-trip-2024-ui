# Dockerfile in the ./python directory
FROM python:3.9-slim

WORKDIR /app
COPY ./src /app/src
COPY requirements.txt /app/
COPY server.py .
COPY database.db .

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "server.py"]

EXPOSE 8080