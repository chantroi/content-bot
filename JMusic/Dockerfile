FROM python:3.10

RUN useradd -m -u 1000 user

COPY --chown=user . /app
WORKDIR /app
RUN apt update && apt install -y default-jdk

RUN pip install flask gunicorn

EXPOSE 7860

CMD gunicorn -b 0.0.0.0:7860 web:app & java -jar JMusicBot.jar