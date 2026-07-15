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

