FROM dart:2.18.2

WORKDIR /app
COPY src/ /app
RUN dart pub get

EXPOSE 5001
ENTRYPOINT ["dart", "run", "/app/app.dart"]
