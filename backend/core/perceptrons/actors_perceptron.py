from dataclasses import dataclass
import json
from typing import Dict, List

from backend.core.perceptrons.prompts import actors_perceive_prompt
from backend.core.perceptrons.base_perceptron import BasePerceptron, PerceptronInput
from backend.schema import ActorNode


# 为参与者感知器定义专属的输入类型
@dataclass
class ActorsPerceptronInput(PerceptronInput):
    user_initial_requirements: str
    actors: List[ActorNode]

class ActorsPerceptron(BasePerceptron[ActorsPerceptronInput]):
    async def perceive(self, input_data: ActorsPerceptronInput) -> Dict:
        response = await self._llm_handler.call_llm(
            prompt=actors_perceive_prompt.replace("{user_initial_requirements}", f"{input_data.user_initial_requirements}"
            ).replace("{actors}", f"{input_data.actors}")
        )
        return json.loads(response)

if __name__ == "__main__":
    import asyncio
    actors_perceptron = ActorsPerceptron()

    user_initial_requirements = "极简纯净本地音乐播放器，不联网、无会员、无广告，只读取电脑本地音乐文件，支持无损格式 Flac/WAV/MP3 播放，自带歌词本地匹配、音效均衡器、歌单自定义、睡眠定时关闭、全局快捷键切歌，界面清爽轻量化，替代臃肿的主流音乐播放器。"

    file_path = "/examples/metadata_and_actors.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    actors = data.get('actors', [])

    async def main():
        actors_perceptron_result = await actors_perceptron.perceive(
            ActorsPerceptronInput(user_initial_requirements, actors)
        )
        # print(type(actors_perceptron).__name__)
    asyncio.run(main())