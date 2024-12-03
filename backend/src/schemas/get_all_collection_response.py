from typing import List

from pydantic import BaseModel

from src.models.collection import Collection


class Item(BaseModel):
    key: str
    name: str
    spec: dict


class GetAllCollectionResponse(BaseModel):
    items: List[Item]

    @staticmethod
    def from_model(collections: List[Collection]) -> dict:
        items = [
            Item(
                key=collection.key,
                name=collection.name,
                spec=collection.spec.spec if collection.spec else {},
            )
            for collection in collections
        ]
        return GetAllCollectionResponse(items=items)
