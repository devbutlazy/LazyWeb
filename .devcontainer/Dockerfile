FROM python:3.11

WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

COPY . .
COPY src/app/main/config/.env ./src/app/main/config/

CMD ["sh", "-c", "python -m src.app.main.web_api --create"]  
# Edit to --upgrade if you want to upgrade revision to main
# Remove the flags if you want to normally start the program (revision should be created and upgraded)