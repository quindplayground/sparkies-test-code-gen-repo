from fastapi import FastAPI

from smoke_health_api.infrastructure.entrypoints.http.health_router import health_router


def register_routes(app: FastAPI) -> None:
    app.include_router(health_router)
