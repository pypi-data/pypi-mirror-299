# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ProtocolRead"]


class ProtocolRead(BaseModel):
    id: int

    external_protocol_id: str = FieldInfo(alias="externalProtocolId")

    title: str
