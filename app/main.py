from fastapi import FastAPI
from app.api.v1.resume import router as resume_router
from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router

app = FastAPI(
    title="IntervuAI API",
    version="1.0.0"
)

app.include_router(
    health_router,
    prefix="/health",
    tags=["Health"]
)

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)
app.include_router(
    resume_router,
    prefix="/api/v1/resume",
    tags=["Resume"]
)

@app.get("/")
def root():
    return {
        "message": "Welcome to IntervuAI"
    }