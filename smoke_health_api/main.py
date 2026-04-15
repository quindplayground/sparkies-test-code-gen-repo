from fastapi import FastAPI

from smoke_health_api.infrastructure.entrypoints.http.health_router import (
    router as health_router,
)


def create_app() -> FastAPI:
    app = FastAPI(title="smoke-health-api")
    app.include_router(health_router)
    return app


app = create_app()
