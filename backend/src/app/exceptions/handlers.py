from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.exceptions.custom import AppException
from app.exceptions.responses import (
    ErrorDetail,
    ErrorResponse,
)

# AppException Handler
async def app_exception_handler(
    request: Request,
    exc: AppException,
):

    response = ErrorResponse(
        error=ErrorDetail(
            code=exc.code,
            message=exc.message,
        ),
        request_id=getattr(
            request.state,
            "request_id",
            None,
        ),
        timestamp=datetime.utcnow(),
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(mode="json"),
    )

# HTTP Exception Handler
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):

    response = ErrorResponse(
        error=ErrorDetail(
            code="HTTP_ERROR",
            message=str(exc.detail),
        ),
        request_id=getattr(
            request.state,
            "request_id",
            None,
        ),
        timestamp=datetime.utcnow(),
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(mode="json"),
    )

# Validation Handler
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):

    response = ErrorResponse(
        error=ErrorDetail(
            code="VALIDATION_ERROR",
            message="Request validation failed",
        ),
        request_id=getattr(
            request.state,
            "request_id",
            None,
        ),
        timestamp=datetime.utcnow(),
    )

    return JSONResponse(
        status_code=422,
        content=response.model_dump(mode="json"),
    )

# Unexpected Exceptions
async def generic_exception_handler(
    request: Request,
    exc: Exception,
):

    response = ErrorResponse(
        error=ErrorDetail(
            code="INTERNAL_SERVER_ERROR",
            message="Unexpected server error",
        ),
        request_id=getattr(
            request.state,
            "request_id",
            None,
        ),
        timestamp=datetime.utcnow(),
    )

    return JSONResponse(
        status_code=500,
        content=response.model_dump(mode="json"),
    )



