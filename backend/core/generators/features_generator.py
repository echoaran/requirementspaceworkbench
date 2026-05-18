from dataclasses import dataclass
import json
from typing import Dict, List

from backend.core.generators.prompts import features_generate_prompt
from backend.core.generators.base_generator import BaseGenerator, GenerateInput
from backend.schemas import ActorNode

# 为特征树生成器定义专属的输入类型
@dataclass
class FeaturesGeneratorInput(GenerateInput):
    user_requirements: str
    actors: List[ActorNode]

class FeaturesGenerator(BaseGenerator[FeaturesGeneratorInput]):
    async def generate(self, input_data: FeaturesGeneratorInput) -> Dict:
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

        response = await self._llm_handler.call_llm(
            prompt=features_generate_prompt.replace(
                "{{user_requirements}}", f"{user_requirements_}").replace(
                "{{actors}}", f"{actors_}"
            ),
            print_log=False,
        )
        return json.loads(response)

if __name__ == "__main__":
    import asyncio
    from backend.schemas import ActorNode

    features_generator = FeaturesGenerator()

    user_requirements = "极简纯净本地音乐播放器，不联网、无会员、无广告，只读取电脑本地音乐文件，支持无损格式 Flac/WAV/MP3 播放，自带歌词本地匹配、音效均衡器、歌单自定义、睡眠定时关闭、全局快捷键切歌，界面清爽轻量化，替代臃肿的主流音乐播放器。"
    test_actors = [
        ActorNode(
            actorId=1,
            actorName="普通用户",
            actorDescription="使用本地音乐播放器进行本地音乐导入、播放、歌单管理、歌词查看、音效调节、定时关闭和快捷切歌的个人用户"
        ),
    ]

    async def main():
         await features_generator.generate(
            FeaturesGeneratorInput(user_requirements, test_actors)
        )
    asyncio.run(main())

    features_generator_result = """
{
  "features": [
    {
      "feature_number": "F001",
      "feature_name": "极简纯净本地音乐播放器",
      "feature_description": "一款不联网、无会员、无广告的轻量化本地音乐播放器，仅支持读取电脑本地音乐文件，提供无损音频播放、歌词匹配、音效调节、歌单管理、睡眠定时和全局快捷键切歌等核心能力，旨在替代臃肿的主流音乐播放器",
      "actor_ids": [
        1
      ],
      "sub_feature_number": [
        "F001-001",
        "F001-002",
        "F001-003",
        "F001-004",
        "F001-005"
      ]
    },
    {
      "feature_number": "F001-001",
      "feature_name": "本地音乐库管理",
      "feature_description": "实现对电脑本地音乐文件的导入、识别、整理与基础浏览能力，作为播放器的内容来源管理中心",
      "actor_ids": [
        1
      ],
      "sub_feature_number": [
        "F001-001-001",
        "F001-001-002",
        "F001-001-003"
      ]
    },
    {
      "feature_number": "F001-001-001",
      "feature_name": "本地文件读取",
      "feature_description": "仅扫描和读取电脑本地存储中的音乐文件，不进行联网获取或云端同步",
      "actor_ids": [
        1
      ],
      "sub_feature_number": []
    },
    {
      "feature_number": "F001-001-002",
      "feature_name": "音频格式识别",
      "feature_description": "支持识别并管理 Flac、WAV、MP3 等本地音频文件格式",
      "actor_ids": [
        1
      ],
      "sub_feature_number": []
    },
    {
      "feature_number": "F001-001-003",
      "feature_name": "音乐库浏览",
      "feature_description": "支持按本地音乐列表进行浏览、查看与选择播放",
      "actor_ids": [
        1
      ],
      "sub_feature_number": []
    },
    {
      "feature_number": "F001-002",
      "feature_name": "音乐播放控制",
      "feature_description": "提供基础且流畅的本地音乐播放与切换控制能力",
      "actor_ids": [
        1
      ],
      "sub_feature_number": [
        "F001-002-001",
        "F001-002-002",
        "F001-002-003"
      ]
    },
    {
      "feature_number": "F001-002-001",
      "feature_name": "播放与暂停控制",
      "feature_description": "支持对本地音乐进行播放、暂停、继续等基础控制",
      "actor_ids": [
        1
      ],
      "sub_feature_number": []
    },
    {
      "feature_number": "F001-002-002",
      "feature_name": "上一首下一首切换",
      "feature_description": "支持在当前播放列表或音乐库中切换上一首、下一首曲目",
      "actor_ids": [
        1
      ],
      "sub_feature_number": []
    },
    {
      "feature_number": "F001-002-003",
      "feature_name": "播放进度与音量控制",
      "feature_description": "支持调节播放进度和基础音量，以满足日常播放操作需求",
      "actor_ids": [
        1
      ],
      "sub_feature_number": []
    },
    {
      "feature_number": "F001-003",
      "feature_name": "歌词与音效设置",
      "feature_description": "提供本地歌词匹配与播放音效调节能力，增强本地听歌体验",
      "actor_ids": [
        1
      ],
      "sub_feature_number": [
        "F001-003-001",
        "F001-003-002"
      ]
    },
    {
      "feature_number": "F001-003-001",
      "feature_name": "本地歌词匹配",
      "feature_description": "支持自动匹配并显示本地歌词内容，便于同步查看歌曲歌词",
      "actor_ids": [
        1
      ],
      "sub_feature_number": []
    },
    {
      "feature_number": "F001-003-002",
      "feature_name": "音效均衡器调节",
      "feature_description": "支持调整均衡器等音效参数，以自定义音乐播放效果",
      "actor_ids": [
        1
      ],
      "sub_feature_number": []
    },
    {
      "feature_number": "F001-004",
      "feature_name": "歌单与播放计划管理",
      "feature_description": "支持用户根据个人偏好自定义歌单，并设置定时停止播放等播放计划",
      "actor_ids": [
        1
      ],
      "sub_feature_number": [
        "F001-004-001",
        "F001-004-002"
      ]
    },
    {
      "feature_number": "F001-004-001",
      "feature_name": "歌单自定义",
      "feature_description": "支持创建、编辑、删除自定义歌单，并将本地歌曲加入对应歌单",
      "actor_ids": [
        1
      ],
      "sub_feature_number": []
    },
    {
      "feature_number": "F001-004-002",
      "feature_name": "睡眠定时关闭",
      "feature_description": "支持设置定时关闭播放器或停止播放，适合睡前自动结束播放",
      "actor_ids": [
        1
      ],
      "sub_feature_number": []
    },
    {
      "feature_number": "F001-005",
      "feature_name": "快捷操作与界面设置",
      "feature_description": "提供全局快捷键操作和清爽轻量化界面，以提升使用便捷性和界面纯净度",
      "actor_ids": [
        1
      ],
      "sub_feature_number": [
        "F001-005-001",
        "F001-005-002"
      ]
    },
    {
      "feature_number": "F001-005-001",
      "feature_name": "全局快捷键切歌",
      "feature_description": "支持在系统任意界面通过全局快捷键进行切歌等播放控制",
      "actor_ids": [
        1
      ],
      "sub_feature_number": []
    },
    {
      "feature_number": "F001-005-002",
      "feature_name": "清爽轻量化界面",
      "feature_description": "提供简洁、纯净、轻量化的界面展示方式，避免冗余功能干扰",
      "actor_ids": [
        1
      ],
      "sub_feature_number": []
    }
  ]
}
"""