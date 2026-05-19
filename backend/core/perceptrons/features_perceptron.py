from dataclasses import dataclass
import json
from typing import Dict, List

from backend.core.perceptrons.prompts import features_perceive_prompt
from backend.core.perceptrons.base_perceptron import BasePerceptron, PerceptronInput
from backend.schemas import ActorNode, FeatureNode


# 为系统功能感知器定义专属的输入类型
@dataclass
class FeaturesPerceptronInput(PerceptronInput):
    user_requirements: str
    actors: List[ActorNode]
    features: List[FeatureNode]

class FeaturesPerceptron(BasePerceptron[FeaturesPerceptronInput]):
    async def perceive(self, input_data: FeaturesPerceptronInput) -> Dict:
        user_requirements_ = input_data.user_requirements

        actors_payload = ActorNode.schema(
            many=True,
            only=("actorId", "actorName", "actorDescription")
        ).dump(input_data.actors)

        actors_ = json.dumps(
            {"actors": actors_payload},
            ensure_ascii=False,
            indent=2
        )

        features_payload = FeatureNode.schema(
            many=True,
            only=("featureId", "featureName", "featureDescription", "actorIds")
        ).dump(node for node in input_data.features if len(node.childrenIds) == 0)      # 筛选出没有孩子的结点，即叶子结点

        features_ = json.dumps(
            {"features": features_payload},
            ensure_ascii=False,
            indent=2
        )

        response = await self._llm_handler.call_llm(
            prompt=features_perceive_prompt.replace(
                "{{user_requirements}}",f"{user_requirements_}").replace(
                "{{actors}}", f"{actors_}").replace(
                "{{features}}", f"{features_}"
            ),
            print_log=False,
        )
        return json.loads(response)

if __name__ == "__main__":
    import asyncio
    features_perceptron = FeaturesPerceptron()

    user_requirements = "极简纯净本地音乐播放器，不联网、无会员、无广告，只读取电脑本地音乐文件，支持无损格式 Flac/WAV/MP3 播放，自带歌词本地匹配、音效均衡器、歌单自定义、睡眠定时关闭、全局快捷键切歌，界面清爽轻量化，替代臃肿的主流音乐播放器。"
    test_actors = [
        ActorNode(
            actorId=1,
            actorName="普通用户",
            actorDescription="使用本地音乐播放器进行本地音乐导入、播放、歌单管理、歌词查看、音效调节、定时关闭和快捷切歌的个人用户"
        ),
    ]
    test_features: List[FeatureNode] = [
        FeatureNode(
            featureId=1,
            featureName="极简纯净本地音乐播放器",
            featureDescription="一款不联网、无会员、无广告的轻量化本地音乐播放器，仅支持读取电脑本地音乐文件，提供无损音频播放、歌词匹配、音效调节、歌单管理、睡眠定时和全局快捷键切歌等核心能力，旨在替代臃肿的主流音乐播放器",
            actorIds=[1],
            childrenIds=[2, 6, 10, 13, 16]
        ),
        FeatureNode(
            featureId=2,
            featureName="本地音乐库管理",
            featureDescription="实现对电脑本地音乐文件的导入、识别、整理与基础浏览能力，作为播放器的内容来源管理中心",
            actorIds=[1],
            childrenIds=[3, 4, 5]
        ),
        FeatureNode(
            featureId=3,
            featureName="本地文件读取",
            featureDescription="仅扫描和读取电脑本地存储中的音乐文件，不进行联网获取或云端同步",
            actorIds=[1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=4,
            featureName="音频格式识别",
            featureDescription="支持识别并管理 Flac、WAV、MP3 等本地音频文件格式",
            actorIds=[1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=5,
            featureName="音乐库浏览",
            featureDescription="支持按本地音乐列表进行浏览、查看与选择播放",
            actorIds=[1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=6,
            featureName="音乐播放控制",
            featureDescription="提供基础且流畅的本地音乐播放与切换控制能力",
            actorIds=[1],
            childrenIds=[7, 8, 9]
        ),
        FeatureNode(
            featureId=7,
            featureName="播放与暂停控制",
            featureDescription="支持对本地音乐进行播放、暂停、继续等基础控制",
            actorIds=[1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=8,
            featureName="上一首下一首切换",
            featureDescription="支持在当前播放列表或音乐库中切换上一首、下一首曲目",
            actorIds=[1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=9,
            featureName="播放进度与音量控制",
            featureDescription="支持调节播放进度和基础音量，以满足日常播放操作需求",
            actorIds=[1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=10,
            featureName="歌词与音效设置",
            featureDescription="提供本地歌词匹配与播放音效调节能力，增强本地听歌体验",
            actorIds=[1],
            childrenIds=[11, 12]
        ),
        FeatureNode(
            featureId=11,
            featureName="本地歌词匹配",
            featureDescription="支持自动匹配并显示本地歌词内容，便于同步查看歌曲歌词",
            actorIds=[1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=12,
            featureName="音效均衡器调节",
            featureDescription="支持调整均衡器等音效参数，以自定义音乐播放效果",
            actorIds=[1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=13,
            featureName="歌单与播放计划管理",
            featureDescription="支持用户根据个人偏好自定义歌单，并设置定时停止播放等播放计划",
            actorIds=[1],
            childrenIds=[14, 15]
        ),
        FeatureNode(
            featureId=14,
            featureName="歌单自定义",
            featureDescription="支持创建、编辑、删除自定义歌单，并将本地歌曲加入对应歌单",
            actorIds=[1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=15,
            featureName="睡眠定时关闭",
            featureDescription="支持设置定时关闭播放器或停止播放，适合睡前自动结束播放",
            actorIds=[1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=16,
            featureName="快捷操作与界面设置",
            featureDescription="提供全局快捷键操作和清爽轻量化界面，以提升使用便捷性和界面纯净度",
            actorIds=[1],
            childrenIds=[17, 18]
        ),
        FeatureNode(
            featureId=17,
            featureName="全局快捷键切歌",
            featureDescription="支持在系统任意界面通过全局快捷键进行切歌等播放控制",
            actorIds=[1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=18,
            featureName="清爽轻量化界面",
            featureDescription="提供简洁、纯净、轻量化的界面展示方式，避免冗余功能干扰",
            actorIds=[1],
            childrenIds=[]
        )
    ]

    async def main():
        features_perceptron_result = await features_perceptron.perceive(
            FeaturesPerceptronInput(user_requirements, test_actors, test_features)
        )
    asyncio.run(main())

    result = """
{
  "perceptionDescription": "不需要"
}
"""