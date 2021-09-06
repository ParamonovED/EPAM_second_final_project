FROM python:3.9

ENV PYTHONUNBUFFERED=1
RUN mkdir -p /code/
COPY . /code/
WORKDIR /code/
RUN pip install -r requirements.txt
