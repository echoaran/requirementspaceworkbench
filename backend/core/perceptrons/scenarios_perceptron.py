from dataclasses import dataclass
import json
from typing import Dict, List

from backend.core.perceptrons.prompts import scenarios_perceive_prompt
from backend.core.perceptrons.base_perceptron import BasePerceptron, PerceptronInput
from backend.schemas import ActorNode, FeatureNode, FlowNode, ScenarioNode


# 为流程感知器定义专属的输入类型
@dataclass
class ScenariosPerceptronInput(PerceptronInput):
    actors: List[ActorNode]
    features: List[FeatureNode]
    flows: List[FlowNode]
    scenarios: List[ScenarioNode]

class ScenariosPerceptron(BasePerceptron[ScenariosPerceptronInput]):
    async def perceive(self, input_data: ScenariosPerceptronInput) -> Dict:
        response = await self._llm_handler.call_llm(
            prompt=scenarios_perceive_prompt.replace("{actors}", f"{input_data.actors}"
            ).replace("{actors}", f"{input_data.actors}"
            ).replace("{features}", f"{input_data.features}"
            ).replace("{flows}", f"{input_data.flows}"
            ).replace("{scenarios}", f"{input_data.scenarios}")
        )
        return json.loads(response)

if __name__ == "__main__":
    import asyncio
    scenarios_perceptron = ScenariosPerceptron()

    user_initial_requirements = "极简纯净本地音乐播放器，不联网、无会员、无广告，只读取电脑本地音乐文件，支持无损格式 Flac/WAV/MP3 播放，自带歌词本地匹配、音效均衡器、歌单自定义、睡眠定时关闭、全局快捷键切歌，界面清爽轻量化，替代臃肿的主流音乐播放器。"
    file_path = "/examples/metadata_and_actors.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    actors = data.get('actors', [])
    file_path = "/backend/examples\\features.json"
    with open(file_path, 'r', encoding='utf-8') as f_1:
        data_1 = json.load(f_1)
    features = data_1.get('features', [])
    file_path_2 = "/backend/examples\\business_objects_and_flows.json"
    with open(file_path_2, 'r', encoding='utf-8') as f_2:
        data_2 = json.load(f_2)
    flows = data_2.get('flows', [])
    file_path_3 = "/backend/examples\\scenarios.json"
    with open(file_path_3, 'r', encoding='utf-8') as f_3:
        data_3 = json.load(f_3)
    scenarios = data_3.get('scenarios', [])

    async def main():
        scenarios_perceptron_result = await scenarios_perceptron.perceive(
            ScenariosPerceptronInput(actors, features, flows, scenarios)
        )
        # print(type(scenarios_perceptron_result).__name__)
    asyncio.run(main())