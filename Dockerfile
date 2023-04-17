FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add gcc python3-dev musl-dev
WORKDIR /backend
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir