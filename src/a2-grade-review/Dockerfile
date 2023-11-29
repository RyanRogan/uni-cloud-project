FROM openjdk:19-alpine3.16

# COPY target/grade-review-0.0.1-SNAPSHOT.jar /grade-review-0.0.1-SNAPSHOT.jar
WORKDIR /grade-review
COPY . /grade-review

RUN ./mvnw clean package

EXPOSE 5003
ENTRYPOINT ["java","-jar","target/grade-review-0.0.1-SNAPSHOT.jar"]