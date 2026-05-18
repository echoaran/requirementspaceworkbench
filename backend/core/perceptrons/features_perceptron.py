from dataclasses import dataclass
import json
from typing import Dict, List

from backend.core.perceptrons.prompts import features_perceive_prompt
from backend.core.perceptrons.base_perceptron import BasePerceptron, PerceptronInput
from backend.schema import ActorNode, FeatureNode


# 为系统功能感知器定义专属的输入类型
@dataclass
class FeaturesPerceptronInput(PerceptronInput):
    user_initial_requirements: str
    actors: List[ActorNode]
    features: List[FeatureNode]

class FeaturesPerceptron(BasePerceptron[FeaturesPerceptronInput]):
    async def perceive(self, input_data: FeaturesPerceptronInput) -> Dict:
        response = await self._llm_handler.call_llm(
            prompt=features_perceive_prompt.replace("{user_initial_requirements}", f"{input_data.user_initial_requirements}"
            ).replace("{actors}", f"{input_data.actors}"
            ).replace("{features}", f"{input_data.features}")
        )
        return json.loads(response)

if __name__ == "__main__":
    import asyncio
    features_perceptron = FeaturesPerceptron()

    user_initial_requirements = "极简纯净本地音乐播放器，不联网、无会员、无广告，只读取电脑本地音乐文件，支持无损格式 Flac/WAV/MP3 播放，自带歌词本地匹配、音效均衡器、歌单自定义、睡眠定时关闭、全局快捷键切歌，界面清爽轻量化，替代臃肿的主流音乐播放器。"
    file_path = "/examples/metadata_and_actors.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    actors = data.get('actors', [])
    file_path = "/backend/examples\\features.json"
    with open(file_path, 'r', encoding='utf-8') as f_1:
        data_1 = json.load(f_1)
    features = data_1.get('features', [])

    async def main():
        features_perceptron_result = await features_perceptron.perceive(
            FeaturesPerceptronInput(user_initial_requirements, actors, features)
        )
        # print(type(features_perceptron_result).__name__)
    asyncio.run(main())