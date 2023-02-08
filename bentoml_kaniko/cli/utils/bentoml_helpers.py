"""
This module contains all function related with BentoML
"""
from typing import List

import bentoml
from bentoml._internal.yatai_rest_api_client.config import (
    YataiClientContext,
    add_context,
    default_context_name,
)
from bentoml._internal.yatai_rest_api_client.yatai import YataiRESTApiClient
from bentoml.exceptions import BentoMLException, CLIException


def make_command(
    svc: bentoml.Service,
    registry: str,
    command: str = "/kaniko/executor",
    cache: bool = False,
) -> List[str]:
    """
    This code creates a list of arguments for a command.
    The first argument is the command itself, followed by the path to the Dockerfile,
    the context (svc.path), and the destination (registry/svc.tag.name:svc.tag.version).
    If cache is set to true, an additional argument --cache=true is added to the
    list of arguments before it is returned.

    Args:
        svc (bentoml.Service): BentoML Service
        registry (str): Name of Container Registry
        command (str, optional): Kaniko command. Defaults to "/kaniko/executor".
        cache (bool, optional): cache or not. Defaults to False.

    Returns:
        List[str]: List of arguments
    """
    args = [
        command,
        f"--dockerfile={svc.path_of('env/docker/Dockerfile')}",
        f"--context={svc.path}",
        f"--destination={registry}/{svc.tag.name}:{svc.tag.version}",
    ]

    if cache:
        args.append("--cache=true",)
    return args


def login_yatai(yatai_endpoint: str, yatai_token: str):
    """
    This code creates a YataiRESTApiClient object with the given endpoint and token.
    It then gets the current user and organization, raising an exception if either is not found.
    Finally, it creates a YataiClientContext object with the default context name, endpoint,
    token, and email from the user. This context is then added to the list of contexts

    Args:
        yatai_endpoint (str): Yatai endpoint
        yatai_token (str): Yatai token

    Raises:
        CLIException: Raised when current user is not found
        CLIException: Raised when current organization is not found
    """

    yatai_rest_client = YataiRESTApiClient(yatai_endpoint, yatai_token)
    user = yatai_rest_client.get_current_user()

    if user is None:
        raise CLIException("current user is not found")

    org = yatai_rest_client.get_current_organization()

    if org is None:
        raise CLIException("current organization is not found")

    ctx = YataiClientContext(
        name=default_context_name,
        endpoint=yatai_endpoint,
        api_token=yatai_token,
        email=user.email,
    )

    add_context(ctx)


def get_bentom_service(bentoml_service: str) -> bentoml.Service:
    """
    This code is used to pull a BentoML service from a remote repository.
    If the service exists, it will be retrieved and returned. If the service
    does not exist, an exception will be raised. The force=True parameter
    indicates that the existing service should be overwritten if it already exists.

    Args:
        bentoml_service (str): Name of BentoML service

    Raises:
        CLIException: raised when BentoMLException was caught

    Returns:
        bentoml.Service: BentoML Service
    """

    bentoml.pull(bentoml_service, force=True)
    try:
        return bentoml.get(bentoml_service)
    except BentoMLException as error:
        raise CLIException from error
