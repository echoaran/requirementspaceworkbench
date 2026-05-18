from dataclasses import dataclass
import json
from typing import Dict,List

from backend.core.generators.prompts import flows_generate_prompt
from backend.core.generators.base_generator import BaseGenerator, GenerateInput
from backend.schemas import FeatureNode, ActorNode

# 为流程生成器定义专属的输入类型
@dataclass
class FlowsGeneratorInput(GenerateInput):
    user_requirements: str
    actors: List[ActorNode]
    features: List[FeatureNode]

class FlowsGenerator(BaseGenerator[FlowsGeneratorInput]):
    async def generate(self, input_data: FlowsGeneratorInput) -> Dict:
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
            prompt=flows_generate_prompt.replace(
                "{{user_requirements}}",f"{user_requirements_}").replace(
                "{{actors}}", f"{actors_}").replace(
                "{{features}}", f"{features_}"
            ),
            print_log=False,
        )
        return json.loads(response)


if __name__ == "__main__":
    import asyncio
    from backend.schemas import FeatureNode, ActorNode
    flows_generator = FlowsGenerator()

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
         await flows_generator.generate(
            FlowsGeneratorInput(user_requirements, test_actors, test_features)
        )
    asyncio.run(main())

    flows_generator_result = """
{
  "business_objects": [
    {
      "business_object_number": "B-001",
      "business_object_name": "音乐文件",
      "business_object_description": "本地存储中的音频文件实体，用于被播放器扫描、识别、播放和管理",
      "business_object_attributes": [
        {
          "business_object_attribute_name": "music_id",
          "business_object_attribute_description": "音乐文件唯一标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "music_20260517_0001"
        },
        {
          "business_object_attribute_name": "file_name",
          "business_object_attribute_description": "音乐文件名称",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "Night_Sky.flac"
        },
        {
          "business_object_attribute_name": "file_path",
          "business_object_attribute_description": "本地文件完整路径",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "D:/Music/Album1/Night_Sky.flac"
        },
        {
          "business_object_attribute_name": "format",
          "business_object_attribute_description": "音频文件格式",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "flac"
        },
        {
          "business_object_attribute_name": "duration",
          "business_object_attribute_description": "音频时长，单位秒",
          "business_object_attribute_type": "integer",
          "business_object_attribute_example": 245
        },
        {
          "business_object_attribute_name": "title",
          "business_object_attribute_description": "歌曲标题",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "Night Sky"
        },
        {
          "business_object_attribute_name": "artist",
          "business_object_attribute_description": "歌手名称",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "Unknown Artist"
        },
        {
          "business_object_attribute_name": "album",
          "business_object_attribute_description": "专辑名称",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "Midnight Collection"
        },
        {
          "business_object_attribute_name": "is_supported",
          "business_object_attribute_description": "是否为播放器支持的格式",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": true
        },
        {
          "business_object_attribute_name": "scan_time",
          "business_object_attribute_description": "最近扫描时间",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "2026-05-17 09:30:00"
        }
      ]
    },
    {
      "business_object_number": "B-002",
      "business_object_name": "音乐库",
      "business_object_description": "本地音乐文件扫描后形成的可浏览、可播放的音乐集合",
      "business_object_attributes": [
        {
          "business_object_attribute_name": "library_id",
          "business_object_attribute_description": "音乐库唯一标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "library_local_001"
        },
        {
          "business_object_attribute_name": "library_name",
          "business_object_attribute_description": "音乐库名称",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "本地音乐库"
        },
        {
          "business_object_attribute_name": "music_count",
          "business_object_attribute_description": "音乐库中的歌曲数量",
          "business_object_attribute_type": "integer",
          "business_object_attribute_example": 328
        },
        {
          "business_object_attribute_name": "supported_formats",
          "business_object_attribute_description": "当前支持的音频格式列表",
          "business_object_attribute_type": "array[string]",
          "business_object_attribute_example": ["flac", "wav", "mp3"]
        },
        {
          "business_object_attribute_name": "last_scan_time",
          "business_object_attribute_description": "最近一次扫描本地文件时间",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "2026-05-17 09:30:00"
        },
        {
          "business_object_attribute_name": "scan_status",
          "business_object_attribute_description": "扫描状态",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "completed"
        }
      ]
    },
    {
      "business_object_number": "B-003",
      "business_object_name": "播放列表",
      "business_object_description": "用于播放控制的曲目集合，可来自音乐库浏览或用户自定义整理",
      "business_object_attributes": [
        {
          "business_object_attribute_name": "playlist_id",
          "business_object_attribute_description": "播放列表唯一标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "playlist_rock_001"
        },
        {
          "business_object_attribute_name": "playlist_name",
          "business_object_attribute_description": "播放列表名称",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "睡前轻音乐"
        },
        {
          "business_object_attribute_name": "song_list",
          "business_object_attribute_description": "播放列表包含的歌曲列表",
          "business_object_attribute_type": "array[string]",
          "business_object_attribute_example": ["music_20260517_0001", "music_20260517_0002"]
        },
        {
          "business_object_attribute_name": "song_count",
          "business_object_attribute_description": "播放列表歌曲数量",
          "business_object_attribute_type": "integer",
          "business_object_attribute_example": 24
        },
        {
          "business_object_attribute_name": "created_time",
          "business_object_attribute_description": "播放列表创建时间",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "2026-05-16 21:00:00"
        },
        {
          "business_object_attribute_name": "updated_time",
          "business_object_attribute_description": "播放列表最后更新时间",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "2026-05-17 08:10:00"
        }
      ]
    },
    {
      "business_object_number": "B-004",
      "business_object_name": "播放状态",
      "business_object_description": "当前播放会话的运行状态，用于记录播放、暂停、进度、音量和当前曲目等信息",
      "business_object_attributes": [
        {
          "business_object_attribute_name": "session_id",
          "business_object_attribute_description": "播放会话唯一标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "session_20260517_01"
        },
        {
          "business_object_attribute_name": "current_music_id",
          "business_object_attribute_description": "当前正在播放的音乐文件标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "music_20260517_0001"
        },
        {
          "business_object_attribute_name": "is_playing",
          "business_object_attribute_description": "是否正在播放",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": true
        },
        {
          "business_object_attribute_name": "play_position",
          "business_object_attribute_description": "当前播放进度，单位秒",
          "business_object_attribute_type": "integer",
          "business_object_attribute_example": 98
        },
        {
          "business_object_attribute_name": "volume",
          "business_object_attribute_description": "当前音量大小，范围通常为0-100",
          "business_object_attribute_type": "integer",
          "business_object_attribute_example": 72
        },
        {
          "business_object_attribute_name": "play_mode",
          "business_object_attribute_description": "播放模式，如顺序、单曲循环、随机",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "sequential"
        },
        {
          "business_object_attribute_name": "start_time",
          "business_object_attribute_description": "本次播放开始时间",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "2026-05-17 09:40:12"
        }
      ]
    },
    {
      "business_object_number": "B-005",
      "business_object_name": "歌词信息",
      "business_object_description": "与本地歌曲匹配得到的歌词内容及其同步显示信息",
      "business_object_attributes": [
        {
          "business_object_attribute_name": "lyric_id",
          "business_object_attribute_description": "歌词信息唯一标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "lyric_20260517_0001"
        },
        {
          "business_object_attribute_name": "music_id",
          "business_object_attribute_description": "对应的音乐文件标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "music_20260517_0001"
        },
        {
          "business_object_attribute_name": "lyric_source_type",
          "business_object_attribute_description": "歌词来源类型，通常为本地歌词文件或内嵌歌词",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "local_file"
        },
        {
          "business_object_attribute_name": "lyric_file_path",
          "business_object_attribute_description": "本地歌词文件路径",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "D:/Music/Album1/Night_Sky.lrc"
        },
        {
          "business_object_attribute_name": "matched",
          "business_object_attribute_description": "是否匹配成功",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": true
        },
        {
          "business_object_attribute_name": "lyrics_text",
          "business_object_attribute_description": "歌词文本内容",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "[00:12.00]When the night sky falls"
        }
      ]
    },
    {
      "business_object_number": "B-006",
      "business_object_name": "音效设置",
      "business_object_description": "播放器的均衡器与音效参数配置，用于个性化音质调节",
      "business_object_attributes": [
        {
          "business_object_attribute_name": "audio_setting_id",
          "business_object_attribute_description": "音效设置唯一标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "audio_setting_default"
        },
        {
          "business_object_attribute_name": "preset_name",
          "business_object_attribute_description": "均衡器预设名称",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "Bass Boost"
        },
        {
          "business_object_attribute_name": "equalizer_bands",
          "business_object_attribute_description": "各频段增益配置",
          "business_object_attribute_type": "array[number]",
          "business_object_attribute_example": [3, 2, 0, -1, 1, 3, 4]
        },
        {
          "business_object_attribute_name": "bass_level",
          "business_object_attribute_description": "低音增强等级",
          "business_object_attribute_type": "integer",
          "business_object_attribute_example": 4
        },
        {
          "business_object_attribute_name": "treble_level",
          "business_object_attribute_description": "高音增强等级",
          "business_object_attribute_type": "integer",
          "business_object_attribute_example": 2
        },
        {
          "business_object_attribute_name": "is_enabled",
          "business_object_attribute_description": "音效是否启用",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": true
        }
      ]
    },
    {
      "business_object_number": "B-007",
      "business_object_name": "睡眠定时任务",
      "business_object_description": "用于在指定时间后自动停止播放或关闭播放器的定时控制任务",
      "business_object_attributes": [
        {
          "business_object_attribute_name": "timer_id",
          "business_object_attribute_description": "定时任务唯一标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "sleep_timer_001"
        },
        {
          "business_object_attribute_name": "mode",
          "business_object_attribute_description": "定时关闭模式，例如停止播放或退出播放器",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "stop_playback"
        },
        {
          "business_object_attribute_name": "remaining_minutes",
          "business_object_attribute_description": "剩余倒计时时长，单位分钟",
          "business_object_attribute_type": "integer",
          "business_object_attribute_example": 30
        },
        {
          "business_object_attribute_name": "target_time",
          "business_object_attribute_description": "预计执行时间",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "2026-05-17 23:30:00"
        },
        {
          "business_object_attribute_name": "is_active",
          "business_object_attribute_description": "定时任务是否启用",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": true
        }
      ]
    },
    {
      "business_object_number": "B-008",
      "business_object_name": "全局快捷键配置",
      "business_object_description": "系统级快捷键映射配置，用于在任意界面执行切歌和播放控制",
      "business_object_attributes": [
        {
          "business_object_attribute_name": "hotkey_id",
          "business_object_attribute_description": "快捷键配置唯一标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "hotkey_global_001"
        },
        {
          "business_object_attribute_name": "previous_track_key",
          "business_object_attribute_description": "上一首快捷键",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "Ctrl+Alt+Left"
        },
        {
          "business_object_attribute_name": "next_track_key",
          "business_object_attribute_description": "下一首快捷键",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "Ctrl+Alt+Right"
        },
        {
          "business_object_attribute_name": "play_pause_key",
          "business_object_attribute_description": "播放/暂停快捷键",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "Ctrl+Alt+Space"
        },
        {
          "business_object_attribute_name": "is_enabled",
          "business_object_attribute_description": "全局快捷键是否启用",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": true
        }
      ]
    },
    {
      "business_object_number": "B-009",
      "business_object_name": "播放器界面配置",
      "business_object_description": "播放器界面的展示与交互配置，体现清爽、轻量化的界面风格",
      "business_object_attributes": [
        {
          "business_object_attribute_name": "ui_config_id",
          "business_object_attribute_description": "界面配置唯一标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "ui_config_default"
        },
        {
          "business_object_attribute_name": "theme_style",
          "business_object_attribute_description": "界面主题风格",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "minimal"
        },
        {
          "business_object_attribute_name": "show_lyrics_panel",
          "business_object_attribute_description": "是否显示歌词面板",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": true
        },
        {
          "business_object_attribute_name": "show_playlist_panel",
          "business_object_attribute_description": "是否显示歌单面板",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": true
        },
        {
          "business_object_attribute_name": "compact_mode",
          "business_object_attribute_description": "是否启用轻量化紧凑模式",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": true
        }
      ]
    }
  ],
  "flows": [
    {
      "flow_name": "本地音乐扫描与识别流程",
      "flow_description": "用户选择本地目录后，系统扫描本地音乐文件并识别支持的音频格式，生成可浏览的音乐库",
      "feature_ids": [3, 4, 5, 18],
      "flow_steps": [
        {
          "step_number": "S-001",
          "step_name": "选择本地音乐目录",
          "step_description": "用户选择一个或多个本地文件夹作为音乐扫描来源",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": [],
          "output_business_object_numbers": ["B-002"],
          "next_steps": ["S-002"]
        },
        {
          "step_number": "S-002",
          "step_name": "扫描本地文件",
          "step_description": "系统扫描所选目录中的本地音频文件，不进行联网获取或云端同步",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-002"],
          "output_business_object_numbers": ["B-001"],
          "next_steps": ["S-003"]
        },
        {
          "step_number": "S-003",
          "step_name": "识别音频格式",
          "step_description": "系统识别扫描到的文件是否为 Flac、WAV、MP3 等支持的格式",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-001"],
          "output_business_object_numbers": ["B-001"],
          "next_steps": ["S-004", "S-005"]
        },
        {
          "step_number": "S-004",
          "step_name": "纳入音乐库",
          "step_description": "将识别成功的音乐文件加入本地音乐库并更新曲目数量",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-001"],
          "output_business_object_numbers": ["B-002"],
          "next_steps": ["S-006"]
        },
        {
          "step_number": "S-005",
          "step_name": "忽略不支持文件",
          "step_description": "系统跳过不支持格式或损坏的文件，并保留扫描结果状态",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-001"],
          "output_business_object_numbers": ["B-002"],
          "next_steps": ["S-006"]
        },
        {
          "step_number": "S-006",
          "step_name": "展示音乐库",
          "step_description": "系统在简洁轻量化界面中展示本地音乐库列表供用户浏览",
          "actor_ids": [1],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-002", "B-009"],
          "output_business_object_numbers": ["B-002"],
          "next_steps": []
        }
      ]
    },
    {
      "flow_name": "音乐播放控制流程",
      "flow_description": "用户从音乐库或播放列表选择歌曲后，进行播放、暂停、进度调节、音量调节以及上一首下一首切换",
      "feature_ids": [5, 7, 8, 9, 18],
      "flow_steps": [
        {
          "step_number": "S-001",
          "step_name": "选择播放曲目",
          "step_description": "用户从音乐库或播放列表中选择一首歌曲开始播放",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-002", "B-003"],
          "output_business_object_numbers": ["B-004"],
          "next_steps": ["S-002"]
        },
        {
          "step_number": "S-002",
          "step_name": "加载并开始播放",
          "step_description": "系统加载本地音频文件并建立播放会话，开始播放当前曲目",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-001", "B-004"],
          "output_business_object_numbers": ["B-004"],
          "next_steps": ["S-003", "S-004", "S-005", "S-006"]
        },
        {
          "step_number": "S-003",
          "step_name": "播放或暂停控制",
          "step_description": "用户在播放过程中执行播放、暂停或继续播放操作",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-004"],
          "output_business_object_numbers": ["B-004"],
          "next_steps": ["S-004", "S-005", "S-006", "S-007"]
        },
        {
          "step_number": "S-004",
          "step_name": "切换上一首或下一首",
          "step_description": "用户通过按钮或快捷键切换当前播放列表中的上一首或下一首歌曲",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-003", "B-004"],
          "output_business_object_numbers": ["B-004"],
          "next_steps": ["S-003", "S-005", "S-006", "S-007"]
        },
        {
          "step_number": "S-005",
          "step_name": "调整播放进度",
          "step_description": "用户拖动进度条调整当前歌曲的播放位置",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-004"],
          "output_business_object_numbers": ["B-004"],
          "next_steps": ["S-003", "S-004", "S-006", "S-007"]
        },
        {
          "step_number": "S-006",
          "step_name": "调节播放音量",
          "step_description": "用户通过音量滑块调节基础音量大小",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-004"],
          "output_business_object_numbers": ["B-004"],
          "next_steps": ["S-003", "S-004", "S-005", "S-007"]
        },
        {
          "step_number": "S-007",
          "step_name": "同步更新播放状态",
          "step_description": "系统实时更新当前播放状态、曲目信息、进度和音量显示",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-004"],
          "output_business_object_numbers": ["B-004"],
          "next_steps": []
        }
      ]
    },
    {
      "flow_name": "本地歌词匹配与显示流程",
      "flow_description": "系统根据当前播放歌曲自动匹配本地歌词文件并在界面中同步显示歌词内容",
      "feature_ids": [7, 11, 18],
      "flow_steps": [
        {
          "step_number": "S-001",
          "step_name": "播放歌曲触发歌词匹配",
          "step_description": "当歌曲开始播放或切换曲目时，系统自动触发歌词匹配流程",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-004", "B-001"],
          "output_business_object_numbers": ["B-005"],
          "next_steps": ["S-002"]
        },
        {
          "step_number": "S-002",
          "step_name": "查找本地歌词文件",
          "step_description": "系统在本地目录中查找与当前歌曲同名或关联的歌词文件",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-001"],
          "output_business_object_numbers": ["B-005"],
          "next_steps": ["S-003", "S-004"]
        },
        {
          "step_number": "S-003",
          "step_name": "匹配成功并解析歌词",
          "step_description": "系统解析匹配到的歌词文件内容并生成可同步展示的歌词信息",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-005"],
          "output_business_object_numbers": ["B-005"],
          "next_steps": ["S-005"]
        },
        {
          "step_number": "S-004",
          "step_name": "匹配失败并标记无歌词",
          "step_description": "系统在未找到歌词文件时标记当前歌曲无可用歌词",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-005"],
          "output_business_object_numbers": ["B-005"],
          "next_steps": ["S-005"]
        },
        {
          "step_number": "S-005",
          "step_name": "显示并同步歌词",
          "step_description": "系统在清爽界面中显示歌词内容，并随播放进度同步高亮当前行",
          "actor_ids": [1],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-005", "B-009"],
          "output_business_object_numbers": ["B-005"],
          "next_steps": []
        }
      ]
    },
    {
      "flow_name": "音效均衡器设置流程",
      "flow_description": "用户调整均衡器和音效参数以自定义本地音乐播放效果",
      "feature_ids": [12, 18],
      "flow_steps": [
        {
          "step_number": "S-001",
          "step_name": "打开音效设置面板",
          "step_description": "用户从播放器界面打开均衡器或音效设置面板",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-009"],
          "output_business_object_numbers": ["B-006"],
          "next_steps": ["S-002"]
        },
        {
          "step_number": "S-002",
          "step_name": "加载当前音效配置",
          "step_description": "系统读取并展示当前启用的均衡器预设和频段参数",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-006"],
          "output_business_object_numbers": ["B-006"],
          "next_steps": ["S-003", "S-004", "S-005"]
        },
        {
          "step_number": "S-003",
          "step_name": "选择或切换预设",
          "step_description": "用户选择适合的均衡器预设方案",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-006"],
          "output_business_object_numbers": ["B-006"],
          "next_steps": ["S-004", "S-005"]
        },
        {
          "step_number": "S-004",
          "step_name": "调整频段参数",
          "step_description": "用户手动调整各频段增益、低音和高音等音效参数",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-006"],
          "output_business_object_numbers": ["B-006"],
          "next_steps": ["S-003", "S-005"]
        },
        {
          "step_number": "S-005",
          "step_name": "应用音效设置",
          "step_description": "系统将当前音效配置应用到正在播放的音乐",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-006", "B-004"],
          "output_business_object_numbers": ["B-006", "B-004"],
          "next_steps": []
        }
      ]
    },
    {
      "flow_name": "歌单自定义管理流程",
      "flow_description": "用户创建、编辑、删除自定义歌单，并将本地歌曲加入或移出歌单",
      "feature_ids": [5, 14, 18],
      "flow_steps": [
        {
          "step_number": "S-001",
          "step_name": "新建歌单",
          "step_description": "用户创建一个新的自定义歌单",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": [],
          "output_business_object_numbers": ["B-003"],
          "next_steps": ["S-002"]
        },
        {
          "step_number": "S-002",
          "step_name": "初始化歌单信息",
          "step_description": "系统生成歌单标识并创建空歌单",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-003"],
          "output_business_object_numbers": ["B-003"],
          "next_steps": ["S-003", "S-004", "S-005", "S-006"]
        },
        {
          "step_number": "S-003",
          "step_name": "编辑歌单名称",
          "step_description": "用户修改歌单名称以便分类管理",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-003"],
          "output_business_object_numbers": ["B-003"],
          "next_steps": ["S-004", "S-005", "S-006"]
        },
        {
          "step_number": "S-004",
          "step_name": "加入本地歌曲",
          "step_description": "用户从音乐库中选择歌曲加入当前歌单",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-002", "B-003"],
          "output_business_object_numbers": ["B-003"],
          "next_steps": ["S-003", "S-005", "S-006"]
        },
        {
          "step_number": "S-005",
          "step_name": "移除歌单歌曲",
          "step_description": "用户将已加入的歌曲从歌单中移除",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-003"],
          "output_business_object_numbers": ["B-003"],
          "next_steps": ["S-003", "S-004", "S-006"]
        },
        {
          "step_number": "S-006",
          "step_name": "删除歌单",
          "step_description": "用户删除不再需要的自定义歌单",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-003"],
          "output_business_object_numbers": [],
          "next_steps": []
        }
      ]
    },
    {
      "flow_name": "睡眠定时关闭流程",
      "flow_description": "用户设置睡眠定时任务，系统在指定时间后自动停止播放或关闭播放器",
      "feature_ids": [15, 7],
      "flow_steps": [
        {
          "step_number": "S-001",
          "step_name": "设置定时时长或结束时间",
          "step_description": "用户输入睡眠定时的时长或目标结束时间",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": [],
          "output_business_object_numbers": ["B-007"],
          "next_steps": ["S-002"]
        },
        {
          "step_number": "S-002",
          "step_name": "创建并启用定时任务",
          "step_description": "系统根据用户设置生成睡眠定时任务并开始倒计时",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-007"],
          "output_business_object_numbers": ["B-007"],
          "next_steps": ["S-003", "S-004"]
        },
        {
          "step_number": "S-003",
          "step_name": "查看剩余时间",
          "step_description": "用户查看当前定时任务的剩余倒计时",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-007"],
          "output_business_object_numbers": ["B-007"],
          "next_steps": ["S-004"]
        },
        {
          "step_number": "S-004",
          "step_name": "到时自动停止播放或退出",
          "step_description": "系统在定时结束后自动停止当前播放或关闭播放器",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-007", "B-004"],
          "output_business_object_numbers": ["B-004", "B-007"],
          "next_steps": []
        }
      ]
    },
    {
      "flow_name": "全局快捷键切歌流程",
      "flow_description": "用户在系统任意界面通过全局快捷键控制播放器切歌、播放和暂停",
      "feature_ids": [7, 8, 17, 18],
      "flow_steps": [
        {
          "step_number": "S-001",
          "step_name": "配置全局快捷键",
          "step_description": "用户在设置界面定义上一首、下一首和播放暂停快捷键",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-008"],
          "output_business_object_numbers": ["B-008"],
          "next_steps": ["S-002"]
        },
        {
          "step_number": "S-002",
          "step_name": "注册系统全局监听",
          "step_description": "系统将快捷键配置注册到操作系统，确保任意界面可响应",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-008"],
          "output_business_object_numbers": ["B-008"],
          "next_steps": ["S-003", "S-004", "S-005"]
        },
        {
          "step_number": "S-003",
          "step_name": "触发上一首快捷键",
          "step_description": "用户按下上一首全局快捷键",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-008", "B-004", "B-003"],
          "output_business_object_numbers": ["B-004"],
          "next_steps": ["S-006"]
        },
        {
          "step_number": "S-004",
          "step_name": "触发下一首快捷键",
          "step_description": "用户按下下一首全局快捷键",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-008", "B-004", "B-003"],
          "output_business_object_numbers": ["B-004"],
          "next_steps": ["S-006"]
        },
        {
          "step_number": "S-005",
          "step_name": "触发播放暂停快捷键",
          "step_description": "用户按下播放或暂停全局快捷键",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-008", "B-004"],
          "output_business_object_numbers": ["B-004"],
          "next_steps": ["S-006"]
        },
        {
          "step_number": "S-006",
          "step_name": "更新播放状态并反馈",
          "step_description": "系统根据快捷键指令切换播放状态并在界面中刷新当前曲目",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-004"],
          "output_business_object_numbers": ["B-004"],
          "next_steps": []
        }
      ]
    },
    {
      "flow_name": "播放器界面轻量化展示流程",
      "flow_description": "系统以清爽、纯净、轻量化的方式展示播放器主界面、音乐库、播放列表、歌词和控制区域",
      "feature_ids": [18, 5, 7, 11, 14, 12, 15, 17],
      "flow_steps": [
        {
          "step_number": "S-001",
          "step_name": "打开播放器主界面",
          "step_description": "用户启动播放器后进入主界面",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": [],
          "output_business_object_numbers": ["B-009"],
          "next_steps": ["S-002"]
        },
        {
          "step_number": "S-002",
          "step_name": "加载界面布局与模块",
          "step_description": "系统按轻量化配置加载音乐库、播放列表、歌词和控制模块",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-009", "B-002", "B-003", "B-005", "B-004"],
          "output_business_object_numbers": ["B-009"],
          "next_steps": ["S-003", "S-004"]
        },
        {
          "step_number": "S-003",
          "step_name": "浏览并选择功能区域",
          "step_description": "用户在清爽界面中切换音乐库、歌单、歌词或音效等功能区域",
          "actor_ids": [1],
          "step_type": "actorAction",
          "input_business_object_numbers": ["B-009"],
          "output_business_object_numbers": ["B-009"],
          "next_steps": ["S-004"]
        },
        {
          "step_number": "S-004",
          "step_name": "保持简洁展示状态",
          "step_description": "系统持续保持低干扰、少冗余的展示状态，确保界面轻量化体验",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_numbers": ["B-009"],
          "output_business_object_numbers": ["B-009"],
          "next_steps": []
        }
      ]
    }
  ]
}

"""