from functools import cached_property
from typing import Union

from alloniaconfigs import Configs as BaseConfigs
from alloniarest import Client
from pydantic import UUID4, BaseModel, Field, HttpUrl


class ConfigSchema(BaseModel):
    USER_TOKEN_ID: Union[str, None] = Field(None, min_length=16, max_length=16)
    USER_TOKEN_SECRET: Union[str, None] = Field(
        None, min_length=32, max_length=32
    )
    TRACK_ID: Union[UUID4, None] = Field(None)
    COMPUTE_API_INTERNAL_URL: Union[HttpUrl, None] = Field(None)


class Configs(BaseConfigs):
    schema = ConfigSchema

    @cached_property
    def compute_api_client(self):
        """Client to request the Compute API."""
        return Client(
            str(self.COMPUTE_API_INTERNAL_URL),
            user_token={
                "id": self.USER_TOKEN_ID,
                "token": self.USER_TOKEN_SECRET,
            },
            trace=False,
        )
