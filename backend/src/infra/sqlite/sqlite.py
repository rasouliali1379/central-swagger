import logging

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from src.config.settings import Config, get_config
from src.services.health import HealthCheck
from src.utils.meta.singleton import SingletonMeta

Base = declarative_base()


class Sqlite(HealthCheck, metaclass=SingletonMeta):

    def __init__(self, config: Config.Database):
        if not hasattr(self, 'initialized'):
            logger = logging.getLogger("startup")
            logger.info("Initializing Sqlite client")
            self.engine = create_async_engine(
                f"sqlite+aiosqlite:///{config.path}",
                echo=False,
                execution_options={"isolation_level": "AUTOCOMMIT"}
            )
            self.SessionLocal = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            self.Base = Base
            self.initialized = True
            logger.info("Sqlite client initialized successfully")

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    def get_session(self) -> AsyncSession:
        return self.SessionLocal()

    async def health(self) -> str | None:
        async with self.SessionLocal() as session:
            try:
                result = await session.execute(text('SELECT 1'))
                if result.scalar() == 1:
                    return None
                return "something wrong with sqlite"
            finally:
                await session.close()

    @property
    def name(self) -> str:
        return "Sqlite"


async def get_sqlite(config: Config = Depends(get_config)) -> Sqlite:
    client = Sqlite(config.sqlite)

    await client.create_tables()

    return client
