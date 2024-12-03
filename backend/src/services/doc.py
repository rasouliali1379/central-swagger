import re
from collections import defaultdict
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


    async def get_all_collections_with_specs(self) -> List[Collection]:
        return await self._collection_repository.get_all_with_specs()

    async def get_all_specs_aggregated(self) -> dict:
        collections = await self._collection_repository.get_all_with_specs()
        return self._merge_swagger_specs(collections)

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

    def _merge_swagger_specs(self, collections):
        """
        Merge multiple Swagger 2.0 JSON specifications into one and resolve name conflicts.
        """
        merged_spec = {
            "swagger": "2.0",
            "info": {
                "title": "Aggregated API",
                "version": "1.0.0"
            },
            "paths": {},
            "definitions": {}
        }

        schema_name_mapping = {}  # Map original schema names to new names
        schema_counter = defaultdict(int)  # Track schema usage per name to resolve conflicts

        for col in collections:
            spec = col.spec.spec
            for path, methods in spec.get("paths", {}).items():
                if path not in merged_spec["paths"]:
                    merged_spec["paths"][path] = {}
                for method, details in methods.items():
                    if method not in merged_spec["paths"][path]:
                        # Update references to schemas in the path details
                        details = self._update_references(details, schema_name_mapping)
                        merged_spec["paths"][path][method] = details

            # Merge definitions
            for schema_name, schema_details in spec.get("definitions", {}).items():
                if schema_name in merged_spec["definitions"]:
                    # Resolve conflict by renaming schema
                    new_schema_name = f"{schema_name}_{schema_counter[schema_name]}"
                    while new_schema_name in merged_spec["definitions"]:
                        schema_counter[schema_name] += 1
                        new_schema_name = f"{schema_name}_{schema_counter[schema_name]}"
                    schema_name_mapping[schema_name] = new_schema_name
                    schema_name = new_schema_name
                else:
                    schema_name_mapping[schema_name] = schema_name

                merged_spec["definitions"][schema_name] = schema_details

        # Apply schema name mapping to all references
        for path, methods in merged_spec["paths"].items():
            for method, details in methods.items():
                merged_spec["paths"][path][method] = self._update_references(details, schema_name_mapping)

        return merged_spec

    def _update_references(self, obj, schema_name_mapping):
        """
        Recursively update $ref fields to point to the new schema names.
        """
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "$ref" and isinstance(value, str) and value.startswith("#/definitions/"):
                    original_name = value.split("/")[-1]
                    if original_name in schema_name_mapping:
                        obj[key] = f"#/definitions/{schema_name_mapping[original_name]}"
                else:
                    self._update_references(value, schema_name_mapping)
        elif isinstance(obj, list):
            for item in obj:
                self._update_references(item, schema_name_mapping)
        return obj


def get_doc_service(config: Config = Depends(get_config),
                    spec_repository: SpecRepository = Depends(get_spec_repository),
                    collection_repository: CollectionRepository = Depends(get_collection_repository)) -> DocService:
    return DocService(config, collection_repository, spec_repository)
