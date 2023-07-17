FROM python:3.9-slim

WORKDIR /app

COPY /requirements.txt .

RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x wait-for-it.sh

CMD ["sh", "-c", "/app/wait-for-it.sh && python load_data.py && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
