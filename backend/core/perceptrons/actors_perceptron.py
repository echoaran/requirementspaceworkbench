from dataclasses import dataclass
import json
from typing import Dict, List

from backend.core.perceptrons.prompts import actors_perceive_prompt
from backend.core.perceptrons.base_perceptron import BasePerceptron, PerceptronInput
from backend.schemas import ActorNode

# 为参与者感知器定义专属的输入类型
@dataclass
class ActorsPerceptronInput(PerceptronInput):
    user_requirements: str
    actors: List[ActorNode]

class ActorsPerceptron(BasePerceptron[ActorsPerceptronInput]):
    async def perceive(self, input_data: ActorsPerceptronInput) -> Dict:

        user_requirements_ = input_data.user_requirements

        actors_payload = ActorNode.schema(
            many=True,
            only=("actorName", "actorDescription")
        ).dump(input_data.actors)

        actors_ = json.dumps(
            {"actors": actors_payload},
            ensure_ascii=False,
            indent=2
        )

        response = await self._llm_handler.call_llm(
            prompt=actors_perceive_prompt.replace(
                "{{user_requirements}}", f"{user_requirements_}").replace(
                "{{actors}}", f"{actors_}"
            ),
            print_log=False,
        )
        return json.loads(response)

if __name__ == "__main__":
    import asyncio
    actors_perceptron = ActorsPerceptron()

    user_requirements = "极简纯净本地音乐播放器，不联网、无会员、无广告，只读取电脑本地音乐文件，支持无损格式 Flac/WAV/MP3 播放，自带歌词本地匹配、音效均衡器、歌单自定义、睡眠定时关闭、全局快捷键切歌，界面清爽轻量化，替代臃肿的主流音乐播放器。"
    test_actors = [
        ActorNode(
            actorId=1,
            actorName="普通用户",
            actorDescription="使用本地音乐播放器进行本地音乐导入、播放、歌单管理、歌词查看、音效调节、定时关闭和快捷切歌的个人用户"
        ),
    ]

    async def main():
        actors_perceptron_result = await actors_perceptron.perceive(
            ActorsPerceptronInput(user_requirements, test_actors)
        )
    asyncio.run(main())

    result = """
{
  "perceptionDescription": "需要补充“音乐文件管理/导入配置用户”和“歌词匹配与播放控制偏好用户”两类参与者描述：一是需求中强调只读取本地音乐文件、支持多格式导入与歌单自定义，当前仅写“本地音乐导入、播放、歌单管理”过于笼统，未体现用户需要对本地曲库进行扫描、筛选、匹配与整理的参与行为；二是需求包含本地歌词自动匹配、音效均衡器、睡眠定时关闭和全局快捷键切歌等功能，说明用户不仅是播放音乐，还会进行歌词校准、音效设置、定时与快捷键偏好配置，需要将这类配置型使用者补充进参与者描述中，以覆盖完整的使用场景。可将普通用户补充描述为“使用本地音乐播放器进行本地曲库导入与管理、歌词匹配、均衡器设置、歌单编辑、睡眠定时和全局快捷键配置的个人用户”。"
}
"""