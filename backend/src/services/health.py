from abc import ABC, abstractmethod

from fastapi import Depends

from src.config.settings import Config, get_config
from src.utils.meta.singleton import SingletonMeta


class HealthCheck(ABC):

    @abstractmethod
    async def health(self) -> str | None:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class HealthService(metaclass=SingletonMeta):
    _config: Config

    def __init__(self, config: Config):
        self._config = config


def get_health_service(config: Config = Depends(get_config)) -> HealthService:
    return HealthService(config)
