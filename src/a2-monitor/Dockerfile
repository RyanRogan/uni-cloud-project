FROM python:3.10

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY src/ /app

# requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5005

ENTRYPOINT ["/app/daemon.sh"]
