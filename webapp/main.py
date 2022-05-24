import logging

from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette_prometheus import PrometheusMiddleware, metrics

from conf.config import settings
from webapp.common.api import misc
from webapp.logger import LOGGING_CONFIG
from webapp.v0.api import scheduler as scheduler_v0


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(PrometheusMiddleware, filter_unhandled_paths=True)
    # CORS Middleware should be last
    # see https://github.com/tiangolo/fastapi/issues/1663
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )


def setup_routers(app: FastAPI) -> None:
    api_router = APIRouter()
    api_router.include_router(scheduler_v0.router, tags=[f'v{scheduler_v0.API_VERSION_MAJOR}'])
    app.include_router(api_router, prefix=f'/v{scheduler_v0.API_VERSION_MAJOR}')
    app.include_router(misc.router)
    app.add_route('/metrics', metrics)


def setup_logger() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)


def create_app() -> FastAPI:
    setup_logger()
    app = FastAPI()
    setup_middleware(app)
    setup_routers(app)
    return app
