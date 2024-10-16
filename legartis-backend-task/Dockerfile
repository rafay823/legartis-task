FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV DB_USERNAME=myuser \
    DB_PASSWORD=mypassword \
    DB_HOST=postgres \
    DB_PORT=5432 \
    DB_NAME=mydb

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
