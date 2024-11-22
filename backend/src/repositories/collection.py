from typing import List

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.orm import aliased

from src.config.settings import Config, get_config
from src.infra.sqlite.sqlite import Sqlite, get_sqlite
from src.models.collection import Collection
from src.models.entities import CollectionEntity, SpecEntity
from src.models.spec import Spec
from src.utils.meta.singleton import SingletonMeta
from src.utils.password.validator import hash_secret


class CollectionRepository(metaclass=SingletonMeta):
    _db: Sqlite
    _config: Config

    def __init__(self, config: Config, db: Sqlite):
        self._config = config
        self._db = db

    async def add(self, collection: CollectionEntity):
        async with self._db.get_session() as session:
            session.add(CollectionEntity(
                name=collection.name,
                key=collection.key,
                secret=hash_secret(collection.secret),
                exposed=collection.exposed,
            ))
            await session.commit()

    async def get(self, key: str) -> Collection:
        async with self._db.get_session() as session:
            result = await session.execute(
                select(CollectionEntity).where(CollectionEntity.key == key)
            )
            collection = result.scalars().first()
            return Collection(
                id=collection.id,
                name=collection.name,
                exposed=collection.exposed,
                key=collection.key,
                secret=collection.secret)

    async def get_keys(self) -> List[str]:
        async with self._db.get_session() as session:
            result = await session.execute(select(CollectionEntity.key))
            keys = result.scalars().all()
            return keys

    async def get_all(self) -> List[Collection]:
        async with self._db.get_session() as session:
            latest_spec = aliased(SpecEntity)

            subquery = (
                select(latest_spec.collection_id, func.max(latest_spec.created_at).label("latest_created_at"))
                .group_by(latest_spec.collection_id)
                .subquery()
            )

            query = (
                select(CollectionEntity, SpecEntity)
                .join(SpecEntity, CollectionEntity.id == SpecEntity.collection_id)
                .join(
                    subquery,
                    (SpecEntity.collection_id == subquery.c.collection_id)
                    & (SpecEntity.created_at == subquery.c.latest_created_at),
                )
            )

            result = await session.execute(query)
            rows = result.all()

            collections = []
            for collection_entity, spec_entity in rows:
                collection = Collection(
                    id=collection_entity.id,
                    name=collection_entity.name,
                    key=collection_entity.key,
                    secret=collection_entity.secret,
                    exposed=collection_entity.exposed,
                    spec=Spec(
                        key=spec_entity.id,
                        spec=spec_entity.spec,
                        collection_id=spec_entity.collection_id,
                    )
                    if spec_entity
                    else None,
                )
                collections.append(collection)

            return collections


def get_collection_repository(config: Config = Depends(get_config),
                              db: Sqlite = Depends(get_sqlite)) -> CollectionRepository:
    return CollectionRepository(config, db)
