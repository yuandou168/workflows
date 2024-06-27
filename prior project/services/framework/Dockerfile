FROM python:slim

RUN pip install fastapi uvicorn psutil

COPY ./app /app

WORKDIR /app

ENTRYPOINT ["python", "-u", "main.py"]