from backend.api.routes.project_creation_routes import (
    router as project_creation_router,
)
from backend.api.routes.blank_project_routes import (
    router as blank_project_router,
)
from backend.api.routes.actor_generation_routes import (
    router as actor_generation_router,
)
from backend.api.routes.feature_generation_routes import (
    router as feature_generation_router,
)
from backend.api.routes.flow_generation_routes import (
    router as flow_generation_router,
)
from backend.api.routes.scenario_generation_routes import (
    router as scenario_generation_router,
)
from backend.api.routes.acceptance_criteria_generation_routes import (
    router as acceptance_criteria_generation_router,
)
from backend.api.routes.scope_generation_routes import (
    router as scope_generation_router,
)

__all__ = [
    "project_creation_router",
    "blank_project_router",
    "actor_generation_router",
    "feature_generation_router",
    "flow_generation_router",
    "scenario_generation_router",
    "acceptance_criteria_generation_router",
    "scope_generation_router",
]
