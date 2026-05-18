from dataclasses import dataclass
import json
from typing import Dict

from backend.core.generators.prompts import actors_generate_prompt
from backend.core.generators.base_generator import BaseGenerator, GenerateInput

# 为参与者生成器定义专属的输入类型
@dataclass
class ActorsGeneratorInput(GenerateInput):
    user_requirements: str

class ActorsGenerator(BaseGenerator[ActorsGeneratorInput]):
    async def generate(self, input_data: ActorsGeneratorInput) -> Dict:
        user_requirements_ = input_data.user_requirements

        response = await self._llm_handler.call_llm(
            prompt=actors_generate_prompt.replace(
                "{{user_requirements}}", user_requirements_
            ),
            print_log=False,
        )
        return json.loads(response)

if __name__ == "__main__":
    import asyncio
    actors_generator = ActorsGenerator()

    user_requirements = "极简纯净本地音乐播放器，不联网、无会员、无广告，只读取电脑本地音乐文件，支持无损格式 Flac/WAV/MP3 播放，自带歌词本地匹配、音效均衡器、歌单自定义、睡眠定时关闭、全局快捷键切歌，界面清爽轻量化，替代臃肿的主流音乐播放器。"

    async def main():
         await actors_generator.generate(
            ActorsGeneratorInput(user_requirements)
        )
    asyncio.run(main())

    actors_generator_result = """
{
  "actors": [
    {
      "actor_name": "普通用户",
      "actor_description": "使用本地音乐播放器进行本地音乐导入、播放、歌单管理、歌词查看、音效调节、定时关闭和快捷切歌的个人用户"
    }
  ]
}
"""