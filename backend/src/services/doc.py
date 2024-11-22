import re
from typing import List

from deepdiff import DeepDiff
from fastapi import Depends

from src.config.settings import Config, get_config
from src.models.collection import Collection
from src.models.spec import Spec
from src.repositories.collection import CollectionRepository, get_collection_repository
from src.repositories.spec import SpecRepository, get_spec_repository
from src.utils.meta.singleton import SingletonMeta
from src.utils.password.generator import generate


class DocService(metaclass=SingletonMeta):
    _config: Config
    _collection_repository: CollectionRepository
    _spec_repository: SpecRepository

    def __init__(self, config: Config, collection_repository: CollectionRepository, spec_repository: SpecRepository):
        self._config = config
        self._collection_repository = collection_repository
        self._spec_repository = spec_repository

    async def create_collection(self, collection: Collection) -> Collection:
        collection.key = await self._generate_collection_key(collection.name)
        collection.secret = generate(self._config.auth.secret_length)
        await self._collection_repository.add(collection)
        return collection

    async def add_spec_to_collection(self, spec: Spec):
        collection = await self._collection_repository.get(spec.key)

        last_spec = await self._spec_repository.get_by_collection_key(spec.key)

        if last_spec:
            diff = DeepDiff(last_spec, spec.spec, ignore_order=True)
            if not diff:
                return
        spec.collection_id = collection.id
        await self._spec_repository.add(spec)

    async def get_all_collections(self) -> List[Collection]:
        return await self._collection_repository.get_all()

    async def _generate_collection_key(self, name: str) -> str:
        normalized_name = name.lower()
        normalized_name = re.sub(r'[^\w\s]', '', normalized_name)
        unique_key = normalized_name.replace(' ', '-')

        original_key = unique_key
        counter = 1

        existing_keys = await self._collection_repository.get_keys()

        while unique_key in existing_keys:
            unique_key = f"{original_key}-{counter}"
            counter += 1

        return unique_key


def get_doc_service(config: Config = Depends(get_config),
                    spec_repository: SpecRepository = Depends(get_spec_repository),
                    collection_repository: CollectionRepository = Depends(get_collection_repository)) -> DocService:
    return DocService(config, collection_repository, spec_repository)
