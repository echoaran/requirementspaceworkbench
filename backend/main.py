from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.api.routes.project_creation_routes import (
    router as project_creation_router,
)
from backend.api.routes.flow_generation_routes import (
    router as flow_generation_router,
)
from backend.api.routes.scenario_generation_routes import (
    router as scenario_generation_router,
)

from backend.database.database import init_db


@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    await init_db()
    yield
    # 【应用关闭时执行】（可选）
    # await close_db()

app = FastAPI(
    title="Requirement Space Workbench API",
    lifespan=lifespan  # 绑定生命周期
)

# 注册路由
app.include_router(project_creation_router)
app.include_router(flow_generation_router)
app.include_router(scenario_generation_router)