from fastapi import FastAPI

from .cors import register_cors
from .gzip import register_gzip
from .request_context import RequestContextMiddleware
from .request_logging import RequestLoggingMiddleware
from .security_headers import SecurityHeadersMiddleware


def register_middleware(app: FastAPI) -> None:
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)

    register_cors(app)
    register_gzip(app)
