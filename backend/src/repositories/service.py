from fastapi import Depends

from src.config.settings import Config, get_config
from src.utils.meta.singleton import SingletonMeta


class ServiceRepository(metaclass=SingletonMeta):

    def __init__(self, config: Config):
        self.config = config

    async def add(self):
        pass

    async def get(self):
        pass


def get_service_repository(config: Config = Depends(get_config)) -> ServiceRepository:
    return ServiceRepository(config)
