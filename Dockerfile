FROM python:3.10

RUN useradd -m -u 1000 user
COPY --chown=user . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
WORKDIR /app/src

ENTRYPOINT python -u main.py & cd /app && python web.py