FROM python:3.11-slim

# Avoids writing .pyc files and shows logs immediately
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create working directory inside the container
WORKDIR /app

# Copy application source
COPY . /app

# Install dependencies if a requirements file is provided
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# The CLI expects to be run from inside src so keep the same entry command
CMD ["python", "src/main.py"]
