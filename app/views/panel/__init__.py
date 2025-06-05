from fastapi import FastAPI

from app.views.panel.endpoints.auth import router as auth_router

app = FastAPI(
    title="User Panel",
    swagger_ui_parameters={"docExpansion": "none"},
)

app.include_router(auth_router, prefix="/panel", tags=["Auth"])
