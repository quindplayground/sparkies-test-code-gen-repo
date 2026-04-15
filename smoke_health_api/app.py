from fastapi import FastAPI

from smoke_health_api.adapters.http.router import health_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(health_router)
    return app
