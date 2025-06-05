FROM python:3.13-slim

RUN useradd -m runner
WORKDIR /home/runner

COPY run.sh .
RUN chmod +x run.sh

USER runner

ENTRYPOINT ["./run.sh"]
