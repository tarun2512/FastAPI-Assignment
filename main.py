import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scripts.constants import AppSpec
from scripts.services import router

app = FastAPI(
    title=AppSpec.name,
    description=AppSpec.description,
    summary=AppSpec.summary,
    version="7.09",
    root_path="/form-mt",
)

if os.environ.get("ENABLE_CORS") in (True, "true", "True") and os.environ.get("CORS_URLS"):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.environ.get("CORS_URLS").split(","),
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE", "PUT"],
        allow_headers=["*"],
    )

app.include_router(router)
