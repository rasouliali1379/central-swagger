import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.routes import health, collection
from src.config.settings import Config

_config = Config()
logger = logging.getLogger()


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Central Swagger service up and running",
                extra={"event_type": "central_swagger_up"})
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"]
)

app.include_router(health.router)
app.include_router(collection.router, prefix="/central-swagger/collections")


@app.exception_handler(Exception)
async def app_error_handler(request, err: Exception):
    status_code = 500
    message = "Something unexpected happened"

    if isinstance(err, HTTPException):
        status_code = err.status_code
        message = err.detail
    else:
        logger.exception(str(err), extra={"event_type": "central_swagger_exception"})

    return JSONResponse(status_code=status_code, content={"message": message})


def init_server() -> FastAPI:
    return app
