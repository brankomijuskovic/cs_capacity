FROM python:3.6-alpine
LABEL maintainer="branko.mijuskovic"
ENV SLEEP=3600
ENV INFLUXDB_HOST=influxdb
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
ENTRYPOINT ["python", "-u", "./app.py"]
