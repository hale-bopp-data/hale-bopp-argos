"""ARGOS-HALE-BOPP — Policy gating engine."""

from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="ARGOS-HALE-BOPP",
    description="Policy enforcement and quality gating engine.",
    version="0.1.0",
)

app.include_router(router)
