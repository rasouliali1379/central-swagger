from fastapi import Depends

from src.config.settings import Config, get_config
from src.utils.meta.singleton import SingletonMeta


class DocService(metaclass=SingletonMeta):
    _config: Config

    def __init__(self, config: Config):
        self._config = config

    def create_service(self):
        pass

    def add_doc(self):
        pass

    def get(self):
        pass

    def get_all(self):
        pass


def get_doc_service(config: Config = Depends(get_config)) -> DocService:
    return DocService(config)
