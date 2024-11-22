from dataclasses import dataclass
from typing import Optional

from src.models.spec import Spec


@dataclass
class Collection:
    name: str
    exposed: bool
    id: Optional[int] = None
    key: Optional[str] = None
    secret: Optional[str] = None
    spec: Optional[Spec] = None
