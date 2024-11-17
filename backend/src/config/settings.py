import os
from enum import Enum


class Env(Enum):
    STAGE = "stage"


class Config:
    _instance = None

    class App:

        def __init__(self):
            self.env = Env(os.getenv("APP_ENV"))

    class Database:
        def __init__(self):
            self.path = os.getenv("CENTRAL_SWAGGER_DB_PATH")

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.app = self.App()
            self.sqlite = self.Database()
            self.initialized = True


def get_config() -> Config:
    return Config()
