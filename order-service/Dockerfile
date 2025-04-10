FROM python:3.11.5-slim-bookworm

RUN apt-get update && apt-get -y install libpq-dev gcc

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python","order_service.py"]