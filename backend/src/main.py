from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.api import v1_router


def create_app() -> FastAPI:
    app_ = FastAPI(
        default_response_class=ORJSONResponse,
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
