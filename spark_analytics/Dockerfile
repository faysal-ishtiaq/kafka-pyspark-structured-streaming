FROM python:3.7-stretch

RUN apt-get update
RUN apt-get install default-jdk -y

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python", "-u", "/app/main.py"]