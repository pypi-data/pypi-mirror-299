from .configs import Configs


class Compute:
    """Send requests to compute API"""

    def __init__(self):
        self._client = Configs.instance.compute_api_client

    def handle_api_call(
        self,
        method: str,
        path: str,
        params: dict,
        fields_to_get: dict,
        depaginate: bool,
    ) -> dict:
        """Depaginates a paginated API call response depending on the params.

        Args:
            method: The request method (get/post/patch/delete).
            path: The request path.
            params: request params. The route must accept "page_number", even if
                it is not specified in those params.
            fields_to_get: the fields to get from the response.
                The dict keys are field names (for example, "count", "objects",
                etc.). The values are also dict, with two keys: 'default', the
                value being the default values for this field, and
                "aggregator", the values being an aggregator
                function (float.__add__, list.__add__, or any function taking
                two arguments of the type of the field and returning a third
                one).
            depaginate: If True, will depaginate the call
        Returns:
            The returned dict will contain the aggregated values found for the
            specified fields_to_get if depaginate is True, else simply
            the 'page_size' first values. "pagination" will not be present.
        """

        def call(current_fields=None):
            resp_ = self._client.request(method, path, params=params)
            resp_.raise_for_status()
            resp_ = resp_.json()
            if not current_fields:
                current_fields = {
                    field_name: resp_.get(field_name, field["default"])
                    for field_name, field in fields_to_get.items()
                }
            else:
                for field_name, field in fields_to_get.items():
                    current_fields[field_name] = field["aggregator"](
                        current_fields[field_name],
                        resp_.get(field_name, field["default"]),
                    )
            return (
                resp_.get("pagination", {}).get("next_page"),
                current_fields,
            )

        if depaginate:
            params["page_size"] = 1000
            params["page_number"] = 1
        else:
            params["page_number"] = params.get("page_number", 1)

        next_page, fields = call()
        if depaginate:
            while next_page:
                params["page_number"] = next_page
                next_page, fields = call(fields)
        return fields

    # Seldon model
    def seldon_deploy_model(
        self,
        track_id,
        model,
        revision=None,
        environment_type=None,
        implementation=None,
    ):
        optional_params = {}
        if revision:
            optional_params["revision"] = revision
        if environment_type:
            optional_params["environment_type"] = environment_type
        if implementation:
            optional_params["implementation"] = implementation

        response = self._client.request(
            "post",
            "/seldon/deploy_model",
            json={
                "track_id": track_id,
                "model": model,
                **optional_params,
            },
        )
        response.raise_for_status()
        return response.json()

    def seldon_get_model_deployment_log(
        self,
        track_id,
        seldon_deployment_id,
        latest_lines=0,
        container="",
        since_time="",
    ):
        optional_params = {}
        if latest_lines:
            optional_params["latest_lines"] = latest_lines
        if container:
            optional_params["container"] = container
        if since_time:
            optional_params["since_time"] = since_time

        return self._client.request(
            "get",
            "/seldon/get_model_deployment_log",
            params={
                "track_id": track_id,
                "seldon_deployment_id": seldon_deployment_id,
                "latest_lines": latest_lines,
                **optional_params,
            },
        )

    def seldon_delete_model_deployment(self, track_id, seldon_deployment_id):
        return self._client.request(
            "delete",
            "/seldon/delete_model_deployment",
            json={
                "track_id": track_id,
                "seldon_deployment_id": seldon_deployment_id,
            },
        )

    def seldon_list_model(
        self, track_id, model="", revision="", depaginate=False
    ):
        params = {}
        if model:
            params["model"] = model
            if revision:
                params["revision"] = revision

        return self.handle_api_call(
            "get",
            f"/seldon/list_model/{track_id}",
            params=params,
            fields_to_get={
                "count": {"default": 0, "aggregator": lambda x, y: x + y},
                "models": {"default": [], "aggregator": lambda x, y: x + y},
            },
            depaginate=depaginate,
        )
