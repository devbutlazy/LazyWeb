python main.py &
sleep 2
uvicorn main:app --host 0.0.0.0 --port 8000