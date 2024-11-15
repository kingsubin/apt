from fastapi import FastAPI
from src.routers import router

from fastapi.responses import ORJSONResponse

def create_app() -> FastAPI:
    app_ = FastAPI(
        default_response_class=ORJSONResponse,
    )

    app_.include_router(router)

    return app_

app = create_app()
@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
