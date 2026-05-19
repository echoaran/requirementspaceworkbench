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
      "feature_description": "一款面向个人用户的轻量化本地音乐播放器，仅读取电脑本地音乐文件，支持无损与常见音频格式播放，提供歌词匹配、音效调节、歌单管理、定时关闭和全局快捷键等功能，强调无联网、无会员、无广告的纯净使用体验",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-001",
      "feature_name": "本地音乐播放管理",
      "feature_description": "实现本地音乐文件的读取、识别、播放与基础播放控制",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-001-001",
      "feature_name": "本地音乐文件读取",
      "feature_description": "仅从电脑本地导入和读取音乐文件，不连接网络获取内容",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-001-002",
      "feature_name": "音频格式播放",
      "feature_description": "支持 Flac、WAV、MP3 等本地音频文件的播放",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-001-003",
      "feature_name": "基础播放控制",
      "feature_description": "支持播放、暂停、上一首、下一首等基础播放操作",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-002",
      "feature_name": "歌词与音效设置",
      "feature_description": "提供本地歌词匹配与播放音效调节功能",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-002-001",
      "feature_name": "本地歌词匹配",
      "feature_description": "自动或手动匹配并显示本地歌词文件",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-002-002",
      "feature_name": "音效均衡器",
      "feature_description": "提供均衡器调节能力，用于调整播放音效表现",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-003",
      "feature_name": "歌单与播放控制",
      "feature_description": "支持用户自定义歌单管理及便捷播放控制设置",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-003-001",
      "feature_name": "歌单自定义",
      "feature_description": "支持创建、编辑、删除和整理用户自定义歌单",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-003-002",
      "feature_name": "播放顺序管理",
      "feature_description": "支持按歌单或单曲进行顺序、随机等播放方式管理",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-004",
      "feature_name": "定时与快捷操作",
      "feature_description": "提供睡眠定时关闭和全局快捷键等便捷操作能力",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-004-001",
      "feature_name": "睡眠定时关闭",
      "feature_description": "支持设置定时关闭播放器或停止播放，适合睡前使用",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-004-002",
      "feature_name": "全局快捷键切歌",
      "feature_description": "支持在系统任意界面通过全局快捷键切换上一首、下一首等播放操作",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-005",
      "feature_name": "界面与纯净体验",
      "feature_description": "提供清爽轻量化的界面设计和纯净无干扰的使用环境",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-005-001",
      "feature_name": "轻量化清爽界面",
      "feature_description": "采用简洁直观的界面布局，降低视觉负担并减少系统资源占用",
      "actor_ids": [
        1
      ]
    },
    {
      "feature_number": "F001-005-002",
      "feature_name": "无联网无广告无会员",
      "feature_description": "软件不提供联网内容、会员服务或广告干扰，保持纯净本地播放体验",
      "actor_ids": [
        1
      ]
    }
  ]
}
"""