# Using a vulnerable base image as specified in security-overview.md
FROM python:3.11.14-slim

WORKDIR /app

# Install system dependencies if any are needed (none for this simple app)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8080

CMD ["python", "app.py"]
