FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY app.py .
COPY environment.py .
COPY models.py .
COPY openenv.yaml .
COPY inference.py .

# Hugging Face Spaces uses port 7860
EXPOSE 7860

# Start FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
