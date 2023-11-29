FROM openjdk:19-alpine3.16

# COPY target/grade-average-0.0.1-SNAPSHOT.jar /grade-average-0.0.1-SNAPSHOT.jar
WORKDIR /grade-average
COPY . /grade-average

RUN ./mvnw clean package -DskipTests

EXPOSE 5002
ENTRYPOINT ["java","-jar","target/grade-average-0.0.1-SNAPSHOT.jar"]