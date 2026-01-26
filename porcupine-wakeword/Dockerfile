FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libasound2-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY wyoming_porcupine.py /app/wyoming_porcupine.py
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 10400/tcp

CMD ["/app/start.sh"]
