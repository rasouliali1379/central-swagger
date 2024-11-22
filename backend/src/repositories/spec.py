from fastapi import Depends
from sqlalchemy import select

from src.config.settings import Config, get_config
from src.infra.sqlite.sqlite import Sqlite, get_sqlite
from src.models.entities import CollectionEntity, SpecEntity
from src.models.spec import Spec
from src.utils.meta.singleton import SingletonMeta


class SpecRepository(metaclass=SingletonMeta):
    _db: Sqlite
    _config: Config

    def __init__(self, config: Config, db: Sqlite):
        self._config = config
        self._db = db

    async def add(self, spec: Spec):
        async with self._db.get_session() as session:
            session.add(SpecEntity(
                collection_id=spec.collection_id,
                spec=spec.spec,
            ))
            await session.commit()

    async def get_all(self):
        pass

    async def get_by_collection_key(self, key: str) -> Spec | None:
        async with self._db.get_session() as session:
            query = (
                select(SpecEntity)
                .join(CollectionEntity, SpecEntity.collection_id == CollectionEntity.id)
                .where(CollectionEntity.key == key)
                .order_by(SpecEntity.id.desc())
                .limit(1)
            )

            result = await session.execute(query)
            spec_result = result.scalar_one_or_none()

            if spec_result:
                return Spec(key=key, spec=spec_result.spec, collection_id=spec_result.collection_id)
        return None


def get_spec_repository(config: Config = Depends(get_config), db: Sqlite = Depends(get_sqlite)) -> SpecRepository:
    return SpecRepository(config, db)
