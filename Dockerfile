FROM python:3.10

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
CMD gunicorn -b 0.0.0.0:8080 web:app & python main.py