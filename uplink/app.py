import sys

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from uplink.config import Config, ConfigError, load_config
from uplink.errors import UplinkError
from uplink.routes import system
from uplink.server import serve

_HTTP_CODES = {404: "not_found", 405: "method_not_allowed"}


def error_response(status: int, code: str, detail: str) -> JSONResponse:
    return JSONResponse({"error": code, "detail": detail}, status_code=status)


def add_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(UplinkError)
    async def uplink_error(request: Request, exc: UplinkError):
        return error_response(exc.status, exc.code, exc.detail)

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException):
        return error_response(
            exc.status_code,
            _HTTP_CODES.get(exc.status_code, "http_error"),
            str(exc.detail),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        return error_response(422, "invalid_request", str(exc.errors()))


def create_app(config: Config) -> FastAPI:
    app = FastAPI(title="uplink", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.config = config
    add_error_handlers(app)
    app.include_router(system.public)
    return app


def main() -> None:
    try:
        config = load_config()
    except ConfigError as e:
        sys.exit(f"uplink: bad config: {e}")
    serve(create_app(config), config.socket_path)
