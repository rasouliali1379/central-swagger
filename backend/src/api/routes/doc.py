
from fastapi import APIRouter, Depends, Response

from src.services.doc import DocService

router = APIRouter()


@router.post('/', status_code=201, response_class=Response)
async def add_favorite(
        req: AddFavoriteRequest,
        user: User = Depends(authorize_user),
        service: DocService = Depends(get_doc_service)
) -> None:
    await service.add_user_favorite_product(Favorite(user_id=user.user_id, product_id=req.product_id))
