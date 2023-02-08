FROM gcr.io/kaniko-project/executor:debug AS kaniko

FROM python:3.8-slim

COPY --from=kaniko /kaniko /kaniko

COPY ./requirements.txt /tmp/requirements.txt

RUN python -m pip install pip --no-cache-dir -U \
    && pip install -r /tmp/requirements.txt --no-cache-dir \
    && rm /tmp/requirements.txt

ENV DOCKER_CONFIG /kaniko/.docker

COPY cli /root/cli

WORKDIR /root

ENTRYPOINT [ "python", "-m", "cli.main" ]