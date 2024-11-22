import bcrypt
from fastapi import HTTPException, Depends, Request

from src.config.settings import Config, get_config
from src.repositories.collection import CollectionRepository, get_collection_repository
from src.utils.password.validator import match


async def authorize(request: Request, config: Config = Depends(get_config),
                    service_repository: CollectionRepository = Depends(get_collection_repository)) -> bool:
    secret = request.headers.get("x-secret")
    key = request.path_params.get("key")
    if secret and key:
        collection = await service_repository.get(key)

        if match(secret, collection.secret):
            request.state.is_admin = False
            return False

    if secret and secret == config.auth.admin_secret:
        request.state.is_admin = True
        return True

    raise HTTPException(status_code=401)
