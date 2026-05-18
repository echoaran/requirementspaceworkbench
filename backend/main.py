import asyncio

from backend.core.generators.actors_generator import ActorsGenerator, ActorsGeneratorInput
from backend.core.generators.features_generator import FeaturesGenerator,FeaturesGeneratorInput

from backend.core.perceptrons.actors_perceptron import ActorsPerceptronInput, ActorsPerceptron
from backend.core.perceptrons.features_perceptron import FeaturesPerceptron, FeaturesPerceptronInput

from backend.schema import RequirementSpace, FeatureNode, ActorNode, PerceptionKindType, PerceptionSlot

Menu = """
*******************************************************
                          菜单
    1. 查看当前需求空间
    2. 查看下一步建议
    3. 执行下一步建议
    4. 进入下一阶段
    5. 结束
*******************************************************
"""

### 模拟what阶段
async def what_stage():
    if_create = input("是否创建项目？（y/n）\n")
    if if_create.lower() != "y":
        return
    user_initial_requirements = input("请输入你的初始需求: \n")

    # 生成参与者
    actors_generator = ActorsGenerator()
    actors_result = await actors_generator.generate(
        ActorsGeneratorInput(user_initial_requirements)
    )

    actors = [
        ActorNode(
            actorId=actor_dict["actor_id"],
            actorName=actor_dict["actor_name"],
            actorDescription=actor_dict["actor_description"]
        )
        for actor_dict in actors_result["actors"]
    ]


    # 生成features tree
    features_generator = FeaturesGenerator()
    result = await features_generator.generate(
        FeaturesGeneratorInput(user_initial_requirements, actors)
    )

    features = [
        FeatureNode(
            featureId=feature_dict["feature_id"],
            featureName=feature_dict["feature_name"],
            featureDescription=feature_dict["feature_description"],
            actorIds=feature_dict["actor_ids"],
            priority=feature_dict["priority"],
            parentId=feature_dict["parent_id"]
        )
        for feature_dict in result["features"]
    ]

    # 创建项目
    requirement_space = RequirementSpace(
        projectName=actors_result["project_name"],
        projectDescription=actors_result["project_description"],
        userInitialRequirements= user_initial_requirements,
        perceptionSlot = None,
        actors=actors,
        features=features
    )

    print(f"项目已创建！")
    need_perceptron = True # 判断是否需要继续提供补充建议，若为 False 不再给出建议，表示可以进入下一阶段。
    while True:
        select = input(f"{Menu}")
        if str(select) == "1":
            print(requirement_space)
            continue
        elif str(select) == "2":
            if requirement_space.perceptionSlot is not None:
                print(requirement_space.perceptionSlot)
            elif not need_perceptron:
                print("没有更多建议了，可以进入下一阶段！")
            else:  # 感知槽是空的并且 need_perceptron 为真就开始感知需要补充的地方。
                actors_perceptron = ActorsPerceptron()
                actors_perceptron_result = await actors_perceptron.perceive(
                    ActorsPerceptronInput(user_initial_requirements, actors)
                )
                if actors_perceptron_result["perceptionDescription"] != "不需要":  # 有潜在的 actors 补充建议
                    perception_slot = PerceptionSlot(PerceptionKindType.ACTOR, actors_perceptron_result.get('perceptionDescription', ""))
                    requirement_space.perceptionSlot = perception_slot
                    print(requirement_space.perceptionSlot)
                else:
                    features_perceive = FeaturesPerceptron()
                    features_perceive_result = await features_perceive.perceive(
                        FeaturesPerceptronInput(user_initial_requirements, actors, features)
                    )
                    if features_perceive_result["perceptionDescription"] != "不需要":  # 有潜在的 features 补充建议
                        perception_slot = PerceptionSlot(PerceptionKindType.FEATURE, features_perceive_result.get('perceptionDescription', ""))
                        requirement_space.perceptionSlot = perception_slot
                        print(requirement_space.perceptionSlot)
                    else:
                        need_perceptron = False
                        print("没有更多建议了，可以进入下一阶段！")
            continue
        elif str(select) == "3":
            print("暂未开发，这里的逻辑就是根据perceptionSlot生成几组候选补充结点")
            continue
        elif str(select) == "4":
            print(f"进入下一阶段 actors 与 features 冻结！\nactors: \n{requirement_space.actors}\nfeatures: \n{requirement_space.features}")
            continue
        else:
            print("GOODBYE!!!!!!!!!!!!!!!!")
            break

if __name__ == "__main__":
    asyncio.run(what_stage())