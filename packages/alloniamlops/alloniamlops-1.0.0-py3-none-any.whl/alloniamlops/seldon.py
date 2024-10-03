"""Functions to easily interact with Seldon"""

import requests

from . import logger
from .compute import Compute
from .configs import Configs

compute_client = Compute()


def deploy_model(model: str, revision=None, implementation=None):
    """Deploy an AleiaModel-encapsulated model.

    Args:
        model: The name of the AleiaModel model to deploy
        revision (optional): The desired version of the model (integer)
        implementation (optional): SKLEARN (default) or TENSORFLOW

    Returns: The Seldon Model deployment record.
    """
    return compute_client.seldon_deploy_model(
        track_id=Configs.instance.track_id,
        model=model,
        revision=revision,
        implementation=f"{implementation}_SERVER" if implementation else None,
    )


def tail(
    seldon_deployment_id: str, latest_lines=0, container="", since_time=""
):
    """Read the last lines of a Seldon model deployment log.

    Args:
        seldon_deployment_id: The id of the Seldon Model Deployment record
        latest_lines (optional): number of lines to extract
        container (optional): "classifier" (default), "seldon-container-engine"
            or "classifier-model-initializer"
        since_time (optional): RFC3339 timestamp from which to show logs

    Returns: logs
    """
    optional_params = {}
    if latest_lines:
        optional_params["latest_lines"] = latest_lines
    if container:
        optional_params["container"] = container
    if since_time:
        optional_params["since_time"] = since_time

    return compute_client.seldon_get_model_deployment_log(
        track_id=Configs.instance.track_id,
        seldon_deployment_id=seldon_deployment_id,
        **optional_params,
    )


def delete_model_deployment(seldon_deployment_id: str):
    """Stop and delete a model deployment.

    Args:
        seldon_deployment_id: The id of the Seldon Model Deployment record

    Returns: An empty response with 204 status code.
    """
    return compute_client.seldon_delete_model_deployment(
        track_id=Configs.instance.track_id,
        seldon_deployment_id=seldon_deployment_id,
    )


def list_model(model="", revision=""):
    """List the Seldon model deployments.

    Args:
        model (optional): filter the results by model name
        revision (optional): if a model name is specified,
            filter by revision number as well (integer)

    Returns: A list of all Seldon models that are up and deployed.
    """
    return compute_client.seldon_list_model(
        track_id=Configs.instance.track_id,
        model=model,
        revision=revision,
        depaginate=True,
    )


def model_predict(seldon_url: str, debug=False, timeout=30, **kwargs):
    """Call the predict function of a deployed Seldon model.

    Args:
        seldon_url: The URL for accessing the deployed Seldon model
        debug: To debug the request sent to the model (defaults to False)
        timeout: Timeout (in s) of the prediction request (defaults to 30s)
        kwargs: will be passed to the predict function,
            e.g.: shape: The shape parameter for model prediction

    Returns: The result from the model prediction.
    """
    url = f"http://{seldon_url}/api/v1.0/predictions"
    headers = {"Content-Type": "application/json"}

    if debug:
        logger.debug(f"Request URL: {url}")
        logger.debug(f"Payload: {kwargs}")

    response = requests.post(url, json=kwargs, headers=headers, timeout=timeout)
    response.raise_for_status()
    if debug:
        logger.debug(f"Response: {response.json()}")
    return response.json()
