FROM python:3.12

WORKDIR /backend

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

COPY . .
COPY config/.env /backend/config/.env

CMD ["sh", "-c", "python -m main.py --create"]
# Edit to --upgrade if you want to upgrade revision to main
# Remove the flags if you want to normally start the program (revision should be created and upgraded)