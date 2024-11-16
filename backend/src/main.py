from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.responses import ORJSONResponse
from src.api import v1_router
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings


def make_middlewares() -> list[Middleware]:
    middlewares = [
        Middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=settings.CORS_METHODS,
            allow_headers=settings.CORS_HEADERS,
        ),
    ]

    return middlewares


def create_app() -> FastAPI:
    app_ = FastAPI(
        default_response_class=ORJSONResponse,
        middleware=make_middlewares(),
    )

    app_.include_router(v1_router)

    return app_


app = create_app()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello, World!"}


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
