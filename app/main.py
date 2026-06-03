from fastapi import FastAPI
from app.api.v1.github import router as github_router
from app.api.v1.resume import router as resume_router
from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.leetcode import router as leetcode_router
from app.api.v1.candidate import router as candidate_router
from app.api.v1.interview import router as interview_router

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
app.include_router(
    github_router,
    prefix="/api/v1/github",
    tags=["GitHub"]

)
app.include_router(
    leetcode_router,
    prefix="/api/v1/leetcode",
    tags=["LeetCode"]

)
app.include_router(
    candidate_router,
    prefix="/api/v1/candidate",
    tags=["Candidate"]
)
app.include_router(
    interview_router,
    prefix="/api/v1/interview",
    tags=["Interview"]
)

@app.get("/")
def root():
    return {
        "message": "Welcome to IntervuAI"
    }