FROM python:3.9.11-slim-bullseye
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /server
WORKDIR /server
ENV PYTHONPATH "${PYTHONPATH}:/"
EXPOSE 8080

RUN apt-get update && \
    apt-get install -y locales --no-install-recommends tzdata && \
    apt-get install -y python3-dev libldap2-dev libsasl2-dev libssl-dev && \
    echo ru_RU.UTF-8 UTF-8 >> /etc/locale.gen && \
    locale-gen
ENV TZ Europe/Moscow
RUN  apt-get update \
  && apt-get install -y wget curl \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /server/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /server/

RUN chmod +x main.py

CMD ["python", "main.py"]
