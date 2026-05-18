from dataclasses import dataclass
import json
from typing import Dict

from backend.core.generators.prompts import scenarios_generate_prompt
from backend.core.generators.base_generator import BaseGenerator, GenerateInput
from backend.schemas import FeatureNode, ActorNode

# 为场景生成器定义专属的输入类型
@dataclass
class ScenariosGeneratorInput(GenerateInput):
    user_requirements: str
    actor: ActorNode
    feature: FeatureNode

class ScenariosGenerator(BaseGenerator[ScenariosGeneratorInput]):
    async def generate(self, input_data: ScenariosGeneratorInput) -> Dict:
        user_requirements_ = input_data.user_requirements

        actor_ = ActorNode.schema(
            only=("actorName", "actorDescription")
        ).dumps(
            input_data.actor,
            indent=2,
            ensure_ascii=False
        )

        feature_ = FeatureNode.schema(
            only=("featureName", "featureDescription")
        ).dumps(
            input_data.feature,
            indent=2,
            ensure_ascii=False
        )

        response = await self._llm_handler.call_llm(
            prompt=scenarios_generate_prompt.replace(
                "{{user_requirements}}", f"{user_requirements_}").replace(
                "{{actor}}",f"{actor_}").replace(
                "{{feature}}", f"{feature_}"
            ),
            print_log=False,
        )
        return json.loads(response)

if __name__ == "__main__":
    import asyncio
    from backend.schemas import FeatureNode, ActorNode
    scenarios_generator = ScenariosGenerator()

    user_requirements = "极简纯净本地音乐播放器，不联网、无会员、无广告，只读取电脑本地音乐文件，支持无损格式 Flac/WAV/MP3 播放，自带歌词本地匹配、音效均衡器、歌单自定义、睡眠定时关闭、全局快捷键切歌，界面清爽轻量化，替代臃肿的主流音乐播放器。"

    test_actor = ActorNode(
        actorId=1,
        actorName="普通用户",
        actorDescription="使用系统进行日常操作的注册用户，拥有基本的浏览、查询和操作权限"
    )

    test_feature = FeatureNode(
        featureId=1,
        featureName="本地文件读取",
        featureDescription="仅从电脑本地读取音乐文件，不依赖网络资源或在线音乐服务",
        actorIds=[1],
        childIds=[],  # 无子功能，为叶子节点
    )

    async def main():
        await scenarios_generator.generate(
            ScenariosGeneratorInput(user_requirements, test_actor, test_feature)
        )

    asyncio.run(main())

    scenarios_generator_result = """
{
  "scenarios": [
    {
      "scenario_name": "从本地文件夹导入音乐文件",
      "scenario_content": "As a 普通用户, I want to 直接从电脑本地文件夹读取音乐文件, So that 我可以在不联网的情况下快速导入自己的歌曲并开始播放"
    },
    {
      "scenario_name": "扫描本地音乐库中的无损和常见音频格式",
      "scenario_content": "As a 普通用户, I want to 从本地读取 Flac、WAV 和 MP3 等音乐文件, So that 我可以统一管理并播放电脑中保存的不同格式音乐"
    },
    {
      "scenario_name": "仅使用本地音乐资源构建播放器曲库",
      "scenario_content": "As a 普通用户, I want to 让播放器只读取电脑本地音乐文件而不依赖在线资源, So that 我可以在离线环境下稳定使用播放器并避免网络内容干扰"
    },
    {
      "scenario_name": "离线浏览本地音乐列表并选择播放",
      "scenario_content": "As a 普通用户, I want to 浏览本地读取到的音乐列表并直接选择歌曲播放, So that 我可以快速找到想听的音乐而无需登录或搜索在线曲库"
    }
  ]
}
"""