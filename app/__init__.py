from starlette.applications import Starlette
from starlette.routing import Mount

from app.views.admin import app as admin_app
from app.views.panel import app as panel_app

app = Starlette(
    routes=[
        Mount("/admin", admin_app),
        Mount("/panel", panel_app),
    ]
)


# TODO: add middleware
