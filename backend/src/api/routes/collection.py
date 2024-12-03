from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.responses import JSONResponse

from src.api.middlewares.auth import authorize
from src.models.collection import Collection
from src.models.spec import Spec
from src.schemas.add_collection_request import AddCollectionRequest
from src.schemas.add_collection_response import AddCollectionResponse
from src.schemas.add_spec_request import AddSpecRequest
from src.schemas.get_all_collection_response import GetAllCollectionResponse
from src.services.doc import DocService, get_doc_service

router = APIRouter()


@router.post('/')
async def add_collection(
        req: AddCollectionRequest,
        is_admin: bool = Depends(authorize),
        service: DocService = Depends(get_doc_service)
) -> AddCollectionResponse:
    if is_admin:
        res = await service.create_collection(Collection(name=req.name, exposed=req.exposed))
        return AddCollectionResponse(key=res.key, secret=res.secret)

    raise HTTPException(status_code=401)


@router.post('/{key}/specs', status_code=201, response_class=Response)
async def add_spec(
        key: str,
        req: AddSpecRequest,
        is_admin: bool = Depends(authorize),
        service: DocService = Depends(get_doc_service)
) -> None:
    await service.add_spec_to_collection(Spec(spec=req.spec, key=key))


@router.get("/all")
async def get_collections(
        service: DocService = Depends(get_doc_service)
) -> GetAllCollectionResponse:
    res = await service.get_all_collections()
    return GetAllCollectionResponse.from_model(res)


@router.get("/")
async def get_collections_with_specs(
        service: DocService = Depends(get_doc_service)
) -> GetAllCollectionResponse:
    res = await service.get_all_collections_with_specs()
    return GetAllCollectionResponse.from_model(res)


@router.get("/aggregated")
async def get_aggregated_specs(
        service: DocService = Depends(get_doc_service)
) -> GetAllCollectionResponse:
    return JSONResponse(content=await service.get_all_specs_aggregated())
