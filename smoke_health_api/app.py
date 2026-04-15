from fastapi import FastAPI

from smoke_health_api.infrastructure.config.wiring import register_routes


def create_app() -> FastAPI:
    app = FastAPI()
    register_routes(app)
    return app
