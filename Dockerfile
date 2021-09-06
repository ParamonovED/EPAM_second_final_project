FROM python:3.9

RUN mkdir -p /code/
COPY . /code/
WORKDIR /code/
RUN pip install -r requirements.txt

CMD ["python","/code/simple_weather/manage.py"]
