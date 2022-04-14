
FROM python:3.10
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . .

# EXPOSE 8000

# CMD ["gunicorn","--bind",":8000", "--workers","3","blogproject.wsgi:application"]

CMD gunicorn blogproject.wsgi:application --bind 0.0.0.0:$PORT