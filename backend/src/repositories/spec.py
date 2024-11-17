from fastapi import Depends

from src.config.settings import Config, get_config
from src.utils.meta.singleton import SingletonMeta


class SpecRepository(metaclass=SingletonMeta):

    def __init__(self, config: Config):
        self.config = config

    async def add(self):
        pass

    async def get_all(self):
        pass


def get_spec_repository(config: Config = Depends(get_config)) -> SpecRepository:
    return SpecRepository(config)
