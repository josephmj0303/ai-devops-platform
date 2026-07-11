from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import get_settings


def register_cors(app):

    settings = get_settings()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
