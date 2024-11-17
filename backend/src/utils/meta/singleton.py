import threading
from abc import ABCMeta


class SingletonBase(type):
    _instances = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instances.get(cls) is None:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class SingletonMeta(SingletonBase, ABCMeta):
    pass
