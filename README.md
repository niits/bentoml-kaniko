# bentoml-kaniko

## Build

`docker build -t bentoml-kaniko-build:latest bentoml_kaniko`

## Usage

```bash
docker run \
    -v ~/.docker/config.json:/kaniko/.docker/config.json:ro \
    -e YATAI_TOKEN=${YATAI_TOKEN} \
    -e YATAI_ENDPOINT=${YATAI_ENDPOINT} \
    bentoml-kaniko-build:latest \
    iris_classifier:puh2bnul6ggyyasc --registry niits
```
