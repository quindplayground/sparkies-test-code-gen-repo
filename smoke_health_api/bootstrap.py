from __future__ import annotations

from fastapi import FastAPI

from smoke_health_api.infrastructure.config.container import AppContainer
from smoke_health_api.infrastructure.entrypoints.http.health_router import (
    create_health_router,
)


def create_app(container: AppContainer | None = None) -> FastAPI:
    resolved = container or AppContainer.default()
    app = FastAPI(title="smoke-health-api")
    health_service = resolved.build_health_application_service()
    app.include_router(create_health_router(health_service))
    return app
