from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
def get_test_endpoint():
    return 200
