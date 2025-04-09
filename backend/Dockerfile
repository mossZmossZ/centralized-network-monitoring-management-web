# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . /app/

# Run FastAPI without reload in production mode
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]