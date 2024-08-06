FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

COPY . .
COPY .config.env .

CMD ["sh", "-c", "uvicorn main:app --host ${HOST} --port ${PORT}"]