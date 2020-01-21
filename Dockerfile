FROM python:3.6

MAINTAINER alansyue b123105@gmail.com

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "app.py"]