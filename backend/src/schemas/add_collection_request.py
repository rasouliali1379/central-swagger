from pydantic import BaseModel


class AddCollectionRequest(BaseModel):
    name: str
    exposed: bool