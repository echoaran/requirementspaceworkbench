from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.schemas.scenario_generation_schema import (
    ScenarioGenerationConfirmResponse,
    ScenarioGenerationDraftDiscardResponse,
    ScenarioGenerationDraftResponse,
    ScenarioGenerationFullDraftCreateRequest,
    ScenarioGenerationSingleDraftCreateRequest,
)
from backend.api.services.scenario_generation_service import (
    ScenarioGenerationService,
)
from backend.database.database import get_session


router = APIRouter(
    prefix="/api/scenario_generation_drafts",
    tags=["scenario_generation"],
)

scenario_generation_service = ScenarioGenerationService()

SCENARIO_GENERATION_ERRORS = {
    "project_not_found",
    "empty_actors",
    "empty_features",
    "empty_leaf_features",
    "feature_id_required",
    "feature_not_found",
    "feature_is_not_leaf",
    "leaf_feature_without_actor",
    "invalid_feature_actor_reference",
    "empty_generation_targets",
    "empty_scenarios",
    "invalid_scenario_payload",
}

@router.post(
    "/full",
    response_model=ScenarioGenerationDraftResponse,
)
async def create_full_scenario_generation_draft(
    request: ScenarioGenerationFullDraftCreateRequest,
    session: AsyncSession = Depends(get_session),
):
    try:
        return await scenario_generation_service.create_full_draft(
            project_id=request.project_id,
            session=session,
        )
    except ValueError as error:
        if str(error) in SCENARIO_GENERATION_ERRORS:
            raise HTTPException(
                status_code=400,
                detail=str(error),
            )
        raise


@router.post(
    "/single",
    response_model=ScenarioGenerationDraftResponse,
)
async def create_single_scenario_generation_draft(
    request: ScenarioGenerationSingleDraftCreateRequest,
    session: AsyncSession = Depends(get_session),
):
    try:
        return await scenario_generation_service.create_single_draft(
            project_id=request.project_id,
            feature_id=request.feature_id,
            session=session,
        )
    except ValueError as error:
        if str(error) in SCENARIO_GENERATION_ERRORS:
            raise HTTPException(
                status_code=400,
                detail=str(error),
            )
        raise


@router.post(
    "/{draft_id}/regenerate",
    response_model=ScenarioGenerationDraftResponse,
)
async def regenerate_scenario_generation_draft(
    draft_id: str,
    session: AsyncSession = Depends(get_session),
):
    try:
        return await scenario_generation_service.regenerate_draft(
            draft_id=draft_id,
            session=session,
        )
    except ValueError as error:
        if str(error) == "draft_not_found":
            raise HTTPException(
                status_code=404,
                detail="draft_not_found",
            )
        if str(error) in SCENARIO_GENERATION_ERRORS:
            raise HTTPException(
                status_code=400,
                detail=str(error),
            )
        raise

@router.post(
    "/{draft_id}/confirm",
    response_model=ScenarioGenerationConfirmResponse,
)
async def confirm_scenario_generation_draft(
    draft_id: str,
    session: AsyncSession = Depends(get_session),
):
    try:
        return await scenario_generation_service.confirm_draft(
            draft_id=draft_id,
            session=session,
        )
    except ValueError as error:
        if str(error) == "draft_not_found":
            raise HTTPException(
                status_code=404,
                detail="draft_not_found",
            )
        if str(error) in SCENARIO_GENERATION_ERRORS:
            raise HTTPException(
                status_code=400,
                detail=str(error),
            )
        raise

@router.delete(
    "/{draft_id}",
    response_model=ScenarioGenerationDraftDiscardResponse,
)
async def discard_scenario_generation_draft(
    draft_id: str,
):
    return await scenario_generation_service.discard_draft(
        draft_id=draft_id,
    )