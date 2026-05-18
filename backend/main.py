from fastapi import FastAPI

from backend.api.routes.project_creation_routes import (
    router as project_creation_router,
)
from backend.database.database import init_db


app = FastAPI(
    title="Requirement Space Workbench API",
)

app.include_router(project_creation_router)


@app.on_event("startup")
async def startup() -> None:
    await init_db()