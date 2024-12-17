FROM python:alpine
COPY . /app
WORKDIR /app
CMD python my_app.py