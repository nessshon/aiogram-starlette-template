from fastapi import FastAPI

from . import example


def app_routers_include(app: FastAPI) -> None:
    """
    Include app routers.
    """
    app.include_router(example.router)


__all__ = [
    "app_routers_include",
]
