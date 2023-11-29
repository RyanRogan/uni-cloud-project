FROM python:3.10

WORKDIR /app
COPY src/ /app
RUN pip install Flask

EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["/app/main.py"]
