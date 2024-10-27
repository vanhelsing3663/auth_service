from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from main.dependencies import init_dependencies

@asynccontextmanager
async def lifespan(_):
    yield


def create_app():
    app = FastAPI(
        swagger_ui_parameters={"docExpansion": "none"},
        title="Authorization Service",
        lifespan=lifespan,
    )

    init_dependencies(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
        allow_headers=[
            "Content-Type",
            "Set-Cookie",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin",
            "Authorization",
        ],
    )
    return app