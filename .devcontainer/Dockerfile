FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

COPY . .
COPY src/app/main/config/.env ./src/app/main/config/

CMD ["sh", "-c", "python -m src.app.main.web_api --upgrade"]