FROM python:3-slim

WORKDIR /programas/ingesta

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ingesta.py .

CMD ["python3", "ingesta.py"]
