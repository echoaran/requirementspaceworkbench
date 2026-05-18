from dataclasses import dataclass
import json
from typing import Dict, List

from backend.core.perceptrons.prompts import flows_perceive_prompt
from backend.core.perceptrons.base_perceptron import BasePerceptron, PerceptronInput
from backend.schema import ActorNode, FeatureNode, FlowNode


# 为流程感知器定义专属的输入类型
@dataclass
class FlowsPerceptronInput(PerceptronInput):
    user_initial_requirements: str
    actors: List[ActorNode]
    features: List[FeatureNode]
    flows: List[FlowNode]

class FlowsPerceptron(BasePerceptron[FlowsPerceptronInput]):
    async def perceive(self, input_data: FlowsPerceptronInput) -> Dict:
        response = await self._llm_handler.call_llm(
            prompt=flows_perceive_prompt.replace("{user_initial_requirements}", f"{input_data.user_initial_requirements}"
            ).replace("{actors}", f"{input_data.actors}")
        )
        return json.loads(response)

if __name__ == "__main__":
    import asyncio
    flows_perceptron = FlowsPerceptron()

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

    async def main():
        flows_perceptron_result = await flows_perceptron.perceive(
            FlowsPerceptronInput(user_initial_requirements, actors, features, flows)
        )
        # print(type(flows_perceptron_result).__name__)
    asyncio.run(main())