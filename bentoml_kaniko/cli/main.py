"""
This code is a Typer app that builds a Docker image from BentoML service.
"""

import subprocess
import sys

import typer

from .utils.bentoml_helpers import get_bentom_service, login_yatai, make_command
from .utils.docker_logging import log_subprocess_output

app = typer.Typer()


@app.command()
def build_bentoml(
    bentoml_service: str = typer.Argument(...),
    registry: str = typer.Option(...),
    yatai_token: str = typer.Option(..., envvar="YATAI_TOKEN"),
    yatai_endpoint: str = typer.Option(..., envvar="YATAI_ENDPOINT"),
):
    """
    It calls the login_yatai() function to log in to Yatai using the provided token and endpoint.
    It then calls get_bentom_service() to get the BentoML service.
    The make_command() function is called to create a command for building the service.

    The command is executed using subprocess.Popen(),
    and its output is logged using log_subprocess_output().
    The exitcode of the process is stored in exitcode,
    which is used to exit the program with sys.exit().

    Args:
        bentoml_service (str): BentoML Tag eg. iris_classifier:puh2bnul6ggyyasc
        registry (str): target registry
        yatai_token (str, optional): read a value from YATAI_TOKEN if it is not provided.
        yatai_endpoint (str, optional): read a value from YATAI_ENDPOINT if it is not provided.
    """

    login_yatai(yatai_endpoint=yatai_endpoint, yatai_token=yatai_token)

    svc = get_bentom_service(bentoml_service=bentoml_service)

    command = make_command(svc, registry=registry)

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    with process.stdout:
        log_subprocess_output(process.stdout)

    exitcode = process.wait()

    sys.exit(exitcode)


if __name__ == "__main__":
    app()
