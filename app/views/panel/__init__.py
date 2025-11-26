import traceback

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database.database import SessionLocal
from app.views.panel.endpoints.auth import router as auth_router
from app.views.panel.endpoints.author import router as author_router
from app.views.panel.endpoints.book import router as book_router
from app.views.panel.endpoints.category import router as category_router

app = FastAPI(
    title="User Panel",
    swagger_ui_parameters={"docExpansion": "none", "persistAuthorization": True},
)

app.include_router(auth_router, prefix="/panel", tags=["Auth"])
app.include_router(category_router, prefix="/category", tags=["Category"])
app.include_router(book_router, prefix="/book", tags=["Book"])
app.include_router(author_router, prefix="/author", tags=["Author"])


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    if isinstance(exc.detail, str):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error_code": exc.status_code, "error_message": exc.detail},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_code": exc.detail.value, "error_message": exc.detail.phrase},
    )


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        request.state.db = SessionLocal()
        return await call_next(request)
    except Exception:
        traceback.print_exc()

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"},
        )
    finally:
        db = getattr(request.state, "db", None)
        if db:
            db.close()


add_pagination(app)
