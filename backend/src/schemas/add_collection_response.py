from pydantic import BaseModel


class AddCollectionResponse(BaseModel):
    key: str
    secret: str