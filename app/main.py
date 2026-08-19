from fastapi import FastAPI

from app.api import auth, health
from app.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
