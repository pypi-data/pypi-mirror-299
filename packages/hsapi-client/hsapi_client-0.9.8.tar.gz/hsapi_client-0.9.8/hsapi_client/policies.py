from pydantic import BaseModel, Field
from typing import Optional
# from datetime import datetime

from .model import HSAPICall
from .schemas import v1Policy


class v1PutPolicyResponse(BaseModel):
    policy: str = Field(alias="policy", default=None)


class Policy(HSAPICall):

    objectPath = "policy"

    def get(self) -> v1Policy:
        response = self.call('get')
        return v1Policy(**response.json())

    def put(self, data: v1Policy) -> v1Policy:
        policy_txt = v1PutPolicyResponse(policy=data.json)
        response = self.call('put', data=policy_txt)
        return v1Policy(**response.json())
