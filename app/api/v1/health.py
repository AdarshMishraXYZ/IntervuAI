from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def health():
    return {
        "status": "ok",
        "message": "IntervuAI Backend Running"
    }