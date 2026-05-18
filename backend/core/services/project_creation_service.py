from uuid import uuid4
from sqlalchemy import insert

from backend.core.generators.actors_generator import (
    ActorsGenerator,
    ActorsGeneratorInput,
)
from backend.core.generators.features_generator import (
    FeaturesGenerator,
    FeaturesGeneratorInput,
)
from backend.schemas import ActorNode


class ProjectCreationService:
    def __init__(self):
        self._drafts: dict[str, dict] = {}
        self._actors_generator = ActorsGenerator()
        self._features_generator = FeaturesGenerator()

    async def create_draft(
        self,
        user_requirements: str,
    ) -> dict:
        draft_id = uuid4().hex

        payload = await self._generate_preview(
            user_requirements=user_requirements,
        )

        payload["draft_id"] = draft_id
        self._drafts[draft_id] = payload
        return payload

    async def regenerate_draft(
        self,
        draft_id: str,
    ) -> dict:
        draft = self._get_draft(draft_id)

        payload = await self._generate_preview(
            user_requirements=draft["user_requirements"],
        )

        payload["draft_id"] = draft_id
        self._drafts[draft_id] = payload
        return payload

    async def confirm_draft(
        self,
        draft_id: str,
        session,
    ) -> dict:
        draft = self._get_draft(draft_id)

        project = await self._persist_project_creation_draft(
            draft=draft,
            session=session,
        )

        self._drafts.pop(draft_id, None)

        return {
            "project_id": project.id,
            "project_name": project.name,
            "project_description": project.description,
            "message": "project_created",
        }

    async def discard_draft(
        self,
        draft_id: str,
    ) -> dict:
        self._drafts.pop(draft_id, None)

        return {
            "draft_id": draft_id,
            "message": "draft_discarded",
        }

    async def _generate_preview(
        self,
        user_requirements: str,
    ) -> dict:
        actors_raw = await self._actors_generator.generate(
            ActorsGeneratorInput(
                user_requirements=user_requirements,
            )
        )

        actor_previews = []
        actor_nodes = []

        for index, raw_actor in enumerate(
            actors_raw["actors"],
            start=1,
        ):
            actor_number = f"A{index:03d}"

            actor_previews.append(
                {
                    "actor_number": actor_number,
                    "actor_name": raw_actor["actor_name"],
                    "actor_description": raw_actor["actor_description"],
                }
            )

            actor_nodes.append(
                ActorNode(
                    actorId=index,
                    actorName=raw_actor["actor_name"],
                    actorDescription=raw_actor["actor_description"],
                )
            )

        features_raw = await self._features_generator.generate(
            FeaturesGeneratorInput(
                user_requirements=user_requirements,
                actors=actor_nodes,
            )
        )

        id_to_actor_number = {
            index: actor["actor_number"]
            for index, actor in enumerate(
                actor_previews,
                start=1,
            )
        }

        feature_previews = []

        for raw_feature in features_raw["features"]:
            feature_previews.append(
                {
                    "feature_number": raw_feature["feature_number"],
                    "feature_name": raw_feature["feature_name"],
                    "feature_description": raw_feature["feature_description"],
                    "actor_numbers": [
                        id_to_actor_number[actor_id]
                        for actor_id in raw_feature.get("actor_ids", [])
                    ],
                    "sub_feature_number": raw_feature.get(
                        "sub_feature_number",
                        [],
                    ),
                }
            )

        root_feature = self._find_root_feature(feature_previews)

        return {
            "user_requirements": user_requirements,
            "project_preview": {
                "project_name": root_feature["feature_name"],
                "project_description": root_feature["feature_description"],
            },
            "actors": actor_previews,
            "features": feature_previews,
        }

    def _find_root_feature(
        self,
        features: list[dict],
    ) -> dict:
        if len(features) == 0:
            raise ValueError("empty_features")

        feature_numbers = {
            feature["feature_number"]
            for feature in features
        }

        child_numbers = set()

        for feature in features:
            child_numbers.update(
                feature.get("sub_feature_number", [])
            )

        root_numbers = feature_numbers - child_numbers

        if len(root_numbers) == 1:
            root_number = next(iter(root_numbers))

            for feature in features:
                if feature["feature_number"] == root_number:
                    return feature

        return features[0]

    def _get_draft(
        self,
        draft_id: str,
    ) -> dict:
        draft = self._drafts.get(draft_id)

        if draft is None:
            raise ValueError("draft_not_found")

        return draft

    async def _persist_project_creation_draft(
        self,
        draft: dict,
        session,
    ):
        from backend.database.model import (
            ActorModel,
            FeatureModel,
            FeatureRelationModel,
            ProjectModel,
            feature_actor_table,
        )

        project_preview = draft["project_preview"]

        project = ProjectModel(
            name=project_preview["project_name"],
            description=project_preview["project_description"],
            user_requirements=draft["user_requirements"],
        )

        session.add(project)
        await session.flush()

        actor_number_to_model = {}

        for actor in draft["actors"]:
            model = ActorModel(
                project_id=project.id,
                name=actor["actor_name"],
                description=actor["actor_description"],
            )

            session.add(model)
            actor_number_to_model[actor["actor_number"]] = model

        await session.flush()

        feature_number_to_model = {}

        for feature in draft["features"]:
            model = FeatureModel(
                project_id=project.id,
                name=feature["feature_name"],
                description=feature["feature_description"],
            )

            session.add(model)
            feature_number_to_model[feature["feature_number"]] = model

        await session.flush()

        feature_actor_rows = []

        for feature in draft["features"]:
            feature_model = feature_number_to_model[
                feature["feature_number"]
            ]

            for actor_number in feature.get("actor_numbers", []):
                actor_model = actor_number_to_model[actor_number]

                feature_actor_rows.append(
                    {
                        "feature_id": feature_model.id,
                        "actor_id": actor_model.id,
                    }
                )

        if feature_actor_rows:
            await session.execute(
                insert(feature_actor_table),
                feature_actor_rows,
            )

        for parent_feature in draft["features"]:
            parent_model = feature_number_to_model[
                parent_feature["feature_number"]
            ]

            for position, child_number in enumerate(
                parent_feature.get("sub_feature_number", []),
                start=1,
            ):
                child_model = feature_number_to_model[child_number]

                relation = FeatureRelationModel(
                    parent_feature_id=parent_model.id,
                    child_feature_id=child_model.id,
                    position=position,
                )

                session.add(relation)

        await session.flush()

        return project