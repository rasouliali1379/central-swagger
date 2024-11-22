from dataclasses import dataclass
from typing import Optional


@dataclass
class Spec:
    key: str
    spec: dict
    collection_id: Optional[int] = None
