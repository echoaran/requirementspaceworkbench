from backend.api.routes.project_creation_routes import (
    router as project_creation_router,
)
from backend.api.routes.flow_generation_routes import (
    router as flow_generation_router,
)
from backend.api.routes.scenario_generation_routes import (
    router as scenario_generation_router,
)

__all__ = [
    "project_creation_router",
    "flow_generation_router",
    "scenario_generation_router",
]