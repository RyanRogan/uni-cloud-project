FROM python:3.10

WORKDIR /app
COPY src/ /app
RUN pip install Flask
RUN pip install requests

EXPOSE 5004

ENTRYPOINT ["python"]
CMD ["/app/main.py"]
