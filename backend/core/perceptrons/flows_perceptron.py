from dataclasses import dataclass
import json
from typing import Dict, List

from backend.core.perceptrons.prompts import flows_perceive_prompt
from backend.core.perceptrons.base_perceptron import BasePerceptron, PerceptronInput
from backend.schemas import ActorNode, FeatureNode, FlowNode, BusinessObjectNode


# 为流程感知器定义专属的输入类型
@dataclass
class FlowsPerceptronInput(PerceptronInput):
    user_requirements: str
    actors: List[ActorNode]
    features: List[FeatureNode]
    business_objects: List[BusinessObjectNode]
    flows: List[FlowNode]

class FlowsPerceptron(BasePerceptron[FlowsPerceptronInput]):
    async def perceive(self, input_data: FlowsPerceptronInput) -> Dict:
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

        business_objects_payload = BusinessObjectNode.schema(
            many=True,
            only=(
                "businessObjectId",
                "businessObjectName",
                "businessObjectDescription",
                "businessObjectAttributes.businessObjectAttributeId",
                "businessObjectAttributes.businessObjectAttributeName",
                "businessObjectAttributes.businessObjectAttributeDescription",
                "businessObjectAttributes.businessObjectAttributeType",
                "businessObjectAttributes.businessObjectAttributeExample",
            ),
        ).dump(input_data.business_objects)

        flows_payload = FlowNode.schema(
            many=True,
            only=(
                "flowId",
                "flowName",
                "flowDescription",
                "featureIds",
                "flowSteps.stepId",
                "flowSteps.stepName",
                "flowSteps.stepDescription",
                "flowSteps.stepType",
                "flowSteps.actorIds",
                "flowSteps.inputBusinessObjectIds",
                "flowSteps.outputBusinessObjectIds",
                "flowSteps.nextStepIds",
            ),
        ).dump(input_data.flows)

        flows_ = json.dumps(
            {
                "business_objects": business_objects_payload,
                "flows": flows_payload,
            },
            ensure_ascii=False,
            indent=2,
        )

        response = await self._llm_handler.call_llm(
            prompt=flows_perceive_prompt.replace(
                "{{user_requirements}}", user_requirements_).replace(
                "{{actors}}", actors_).replace(
                "{{features}}", features_).replace(
                "{{flows}}", flows_),
            print_log=True,
        )

        return json.loads(response)

if __name__ == "__main__":
    import asyncio
    from backend.schemas import (
        BusinessObjectAttributeNode,
        BusinessObjectNode,
        FlowNode,
        FlowStepNode,
        FlowStepType,
    )

    flows_perceptron = FlowsPerceptron()

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



    test_business_objects = [
        BusinessObjectNode(
            businessObjectId=1,
            businessObjectName="音乐文件",
            businessObjectDescription="本地存储中的音频文件实体，用于被播放器扫描、识别、播放和管理",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=1,
                    businessObjectAttributeName="music_id",
                    businessObjectAttributeDescription="音乐文件唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="music_20260517_0001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=2,
                    businessObjectAttributeName="file_name",
                    businessObjectAttributeDescription="音乐文件名称",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="Night_Sky.flac",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=3,
                    businessObjectAttributeName="file_path",
                    businessObjectAttributeDescription="本地文件完整路径",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="D:/Music/Album1/Night_Sky.flac",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=4,
                    businessObjectAttributeName="format",
                    businessObjectAttributeDescription="音频文件格式",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="flac",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=5,
                    businessObjectAttributeName="duration",
                    businessObjectAttributeDescription="音频时长，单位秒",
                    businessObjectAttributeType="integer",
                    businessObjectAttributeExample="245",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=6,
                    businessObjectAttributeName="title",
                    businessObjectAttributeDescription="歌曲标题",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="Night Sky",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=7,
                    businessObjectAttributeName="artist",
                    businessObjectAttributeDescription="歌手名称",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="Unknown Artist",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=8,
                    businessObjectAttributeName="album",
                    businessObjectAttributeDescription="专辑名称",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="Midnight Collection",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=9,
                    businessObjectAttributeName="is_supported",
                    businessObjectAttributeDescription="是否为播放器支持的格式",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=110,
                    businessObjectAttributeName="scan_time",
                    businessObjectAttributeDescription="最近扫描时间",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="2026-05-17 09:30:00",
                ),
            ],
        ),
        BusinessObjectNode(
            businessObjectId=2,
            businessObjectName="音乐库",
            businessObjectDescription="本地音乐文件扫描后形成的可浏览、可播放的音乐集合",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=1,
                    businessObjectAttributeName="library_id",
                    businessObjectAttributeDescription="音乐库唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="library_local_001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=2,
                    businessObjectAttributeName="library_name",
                    businessObjectAttributeDescription="音乐库名称",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="本地音乐库",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=3,
                    businessObjectAttributeName="music_count",
                    businessObjectAttributeDescription="音乐库中的歌曲数量",
                    businessObjectAttributeType="integer",
                    businessObjectAttributeExample="328",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=4,
                    businessObjectAttributeName="supported_formats",
                    businessObjectAttributeDescription="当前支持的音频格式列表",
                    businessObjectAttributeType="array[string]",
                    businessObjectAttributeExample="['flac', 'wav', 'mp3']",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=5,
                    businessObjectAttributeName="last_scan_time",
                    businessObjectAttributeDescription="最近一次扫描本地文件时间",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="2026-05-17 09:30:00",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=6,
                    businessObjectAttributeName="scan_status",
                    businessObjectAttributeDescription="扫描状态",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="completed",
                ),
            ],
        ),
        BusinessObjectNode(
            businessObjectId=3,
            businessObjectName="播放列表",
            businessObjectDescription="用于播放控制的曲目集合，可来自音乐库浏览或用户自定义整理",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=1,
                    businessObjectAttributeName="playlist_id",
                    businessObjectAttributeDescription="播放列表唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="playlist_rock_001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=2,
                    businessObjectAttributeName="playlist_name",
                    businessObjectAttributeDescription="播放列表名称",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="睡前轻音乐",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=3,
                    businessObjectAttributeName="song_list",
                    businessObjectAttributeDescription="播放列表包含的歌曲列表",
                    businessObjectAttributeType="array[string]",
                    businessObjectAttributeExample="['music_20260517_0001', 'music_20260517_0002']",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=4,
                    businessObjectAttributeName="song_count",
                    businessObjectAttributeDescription="播放列表歌曲数量",
                    businessObjectAttributeType="integer",
                    businessObjectAttributeExample="24",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=5,
                    businessObjectAttributeName="created_time",
                    businessObjectAttributeDescription="播放列表创建时间",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="2026-05-16 21:00:00",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=6,
                    businessObjectAttributeName="updated_time",
                    businessObjectAttributeDescription="播放列表最后更新时间",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="2026-05-17 08:10:00",
                ),
            ],
        ),
        BusinessObjectNode(
            businessObjectId=4,
            businessObjectName="播放状态",
            businessObjectDescription="当前播放会话的运行状态，用于记录播放、暂停、进度、音量和当前曲目等信息",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=1,
                    businessObjectAttributeName="session_id",
                    businessObjectAttributeDescription="播放会话唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="session_20260517_01",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=2,
                    businessObjectAttributeName="current_music_id",
                    businessObjectAttributeDescription="当前正在播放的音乐文件标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="music_20260517_0001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=3,
                    businessObjectAttributeName="is_playing",
                    businessObjectAttributeDescription="是否正在播放",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=4,
                    businessObjectAttributeName="play_position",
                    businessObjectAttributeDescription="当前播放进度，单位秒",
                    businessObjectAttributeType="integer",
                    businessObjectAttributeExample="98",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=5,
                    businessObjectAttributeName="volume",
                    businessObjectAttributeDescription="当前音量大小，范围通常为0-100",
                    businessObjectAttributeType="integer",
                    businessObjectAttributeExample="72",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=6,
                    businessObjectAttributeName="play_mode",
                    businessObjectAttributeDescription="播放模式，如顺序、单曲循环、随机",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="sequential",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=7,
                    businessObjectAttributeName="start_time",
                    businessObjectAttributeDescription="本次播放开始时间",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="2026-05-17 09:40:12",
                ),
            ],
        ),
        BusinessObjectNode(
            businessObjectId=5,
            businessObjectName="歌词信息",
            businessObjectDescription="与本地歌曲匹配得到的歌词内容及其同步显示信息",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=1,
                    businessObjectAttributeName="lyric_id",
                    businessObjectAttributeDescription="歌词信息唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="lyric_20260517_0001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=2,
                    businessObjectAttributeName="music_id",
                    businessObjectAttributeDescription="对应的音乐文件标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="music_20260517_0001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=3,
                    businessObjectAttributeName="lyric_source_type",
                    businessObjectAttributeDescription="歌词来源类型，通常为本地歌词文件或内嵌歌词",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="local_file",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=4,
                    businessObjectAttributeName="lyric_file_path",
                    businessObjectAttributeDescription="本地歌词文件路径",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="D:/Music/Album1/Night_Sky.lrc",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=5,
                    businessObjectAttributeName="matched",
                    businessObjectAttributeDescription="是否匹配成功",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=6,
                    businessObjectAttributeName="lyrics_text",
                    businessObjectAttributeDescription="歌词文本内容",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="[00:12.00]When the night sky falls",
                ),
            ],
        ),
        BusinessObjectNode(
            businessObjectId=6,
            businessObjectName="音效设置",
            businessObjectDescription="播放器的均衡器与音效参数配置，用于个性化音质调节",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=1,
                    businessObjectAttributeName="audio_setting_id",
                    businessObjectAttributeDescription="音效设置唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="audio_setting_default",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=2,
                    businessObjectAttributeName="preset_name",
                    businessObjectAttributeDescription="均衡器预设名称",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="Bass Boost",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=3,
                    businessObjectAttributeName="equalizer_bands",
                    businessObjectAttributeDescription="各频段增益配置",
                    businessObjectAttributeType="array[number]",
                    businessObjectAttributeExample="[3, 2, 0, -1, 1, 3, 4]",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=4,
                    businessObjectAttributeName="bass_level",
                    businessObjectAttributeDescription="低音增强等级",
                    businessObjectAttributeType="integer",
                    businessObjectAttributeExample="4",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=5,
                    businessObjectAttributeName="treble_level",
                    businessObjectAttributeDescription="高音增强等级",
                    businessObjectAttributeType="integer",
                    businessObjectAttributeExample="2",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=6,
                    businessObjectAttributeName="is_enabled",
                    businessObjectAttributeDescription="音效是否启用",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
            ],
        ),
        BusinessObjectNode(
            businessObjectId=7,
            businessObjectName="睡眠定时任务",
            businessObjectDescription="用于在指定时间后自动停止播放或关闭播放器的定时控制任务",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=1,
                    businessObjectAttributeName="timer_id",
                    businessObjectAttributeDescription="定时任务唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="sleep_timer_001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=2,
                    businessObjectAttributeName="mode",
                    businessObjectAttributeDescription="定时关闭模式，例如停止播放或退出播放器",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="stop_playback",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=3,
                    businessObjectAttributeName="remaining_minutes",
                    businessObjectAttributeDescription="剩余倒计时时长，单位分钟",
                    businessObjectAttributeType="integer",
                    businessObjectAttributeExample="30",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=4,
                    businessObjectAttributeName="target_time",
                    businessObjectAttributeDescription="预计执行时间",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="2026-05-17 23:30:00",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=5,
                    businessObjectAttributeName="is_active",
                    businessObjectAttributeDescription="定时任务是否启用",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
            ],
        ),
        BusinessObjectNode(
            businessObjectId=8,
            businessObjectName="全局快捷键配置",
            businessObjectDescription="系统级快捷键映射配置，用于在任意界面执行切歌和播放控制",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=1,
                    businessObjectAttributeName="hotkey_id",
                    businessObjectAttributeDescription="快捷键配置唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="hotkey_global_001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=2,
                    businessObjectAttributeName="previous_track_key",
                    businessObjectAttributeDescription="上一首快捷键",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="Ctrl+Alt+Left",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=3,
                    businessObjectAttributeName="next_track_key",
                    businessObjectAttributeDescription="下一首快捷键",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="Ctrl+Alt+Right",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=4,
                    businessObjectAttributeName="play_pause_key",
                    businessObjectAttributeDescription="播放/暂停快捷键",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="Ctrl+Alt+Space",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=5,
                    businessObjectAttributeName="is_enabled",
                    businessObjectAttributeDescription="全局快捷键是否启用",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
            ],
        ),
        BusinessObjectNode(
            businessObjectId=9,
            businessObjectName="播放器界面配置",
            businessObjectDescription="播放器界面的展示与交互配置，体现清爽、轻量化的界面风格",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=1,
                    businessObjectAttributeName="ui_config_id",
                    businessObjectAttributeDescription="界面配置唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="ui_config_default",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=2,
                    businessObjectAttributeName="theme_style",
                    businessObjectAttributeDescription="界面主题风格",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="minimal",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=3,
                    businessObjectAttributeName="show_lyrics_panel",
                    businessObjectAttributeDescription="是否显示歌词面板",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=4,
                    businessObjectAttributeName="show_playlist_panel",
                    businessObjectAttributeDescription="是否显示歌单面板",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=5,
                    businessObjectAttributeName="compact_mode",
                    businessObjectAttributeDescription="是否启用轻量化紧凑模式",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
            ],
        ),
    ]

    test_flows = [
        FlowNode(
            flowId=1,
            flowName="本地音乐扫描与识别流程",
            flowDescription="用户选择本地目录后，系统扫描本地音乐文件并识别支持的音频格式，生成可浏览的音乐库",
            featureIds=[3, 4, 5, 18],
            flowSteps=[
                FlowStepNode(
                    stepId=1,
                    stepName="选择本地音乐目录",
                    stepDescription="用户选择一个或多个本地文件夹作为音乐扫描来源",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[],
                    outputBusinessObjectIds=[2],
                    nextStepIds=[2],
                ),
                FlowStepNode(
                    stepId=2,
                    stepName="扫描本地文件",
                    stepDescription="系统扫描所选目录中的本地音频文件，不进行联网获取或云端同步",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[2],
                    outputBusinessObjectIds=[1],
                    nextStepIds=[3],
                ),
                FlowStepNode(
                    stepId=3,
                    stepName="识别音频格式",
                    stepDescription="系统识别扫描到的文件是否为 Flac、WAV、MP3 等支持的格式",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[1],
                    outputBusinessObjectIds=[1],
                    nextStepIds=[4, 5],
                ),
                FlowStepNode(
                    stepId=4,
                    stepName="纳入音乐库",
                    stepDescription="将识别成功的音乐文件加入本地音乐库并更新曲目数量",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[1],
                    outputBusinessObjectIds=[2],
                    nextStepIds=[6],
                ),
                FlowStepNode(
                    stepId=5,
                    stepName="忽略不支持文件",
                    stepDescription="系统跳过不支持格式或损坏的文件，并保留扫描结果状态",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[1],
                    outputBusinessObjectIds=[2],
                    nextStepIds=[6],
                ),
                FlowStepNode(
                    stepId=6,
                    stepName="展示音乐库",
                    stepDescription="系统在简洁轻量化界面中展示本地音乐库列表供用户浏览",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[2, 9],
                    outputBusinessObjectIds=[2],
                    nextStepIds=[],
                ),
            ],
        ),
        FlowNode(
            flowId=2,
            flowName="音乐播放控制流程",
            flowDescription="用户从音乐库或播放列表选择歌曲后，进行播放、暂停、进度调节、音量调节以及上一首下一首切换",
            featureIds=[5, 7, 8, 9, 18],
            flowSteps=[
                FlowStepNode(
                    stepId=1,
                    stepName="选择播放曲目",
                    stepDescription="用户从音乐库或播放列表中选择一首歌曲开始播放",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[2, 3],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[2],
                ),
                FlowStepNode(
                    stepId=2,
                    stepName="加载并开始播放",
                    stepDescription="系统加载本地音频文件并建立播放会话，开始播放当前曲目",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[1, 4],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[3, 4, 5, 6],
                ),
                FlowStepNode(
                    stepId=3,
                    stepName="播放或暂停控制",
                    stepDescription="用户在播放过程中执行播放、暂停或继续播放操作",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[4],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[4, 5, 6, 7],
                ),
                FlowStepNode(
                    stepId=4,
                    stepName="切换上一首或下一首",
                    stepDescription="用户通过按钮或快捷键切换当前播放列表中的上一首或下一首歌曲",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[3, 4],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[3, 5, 6, 7],
                ),
                FlowStepNode(
                    stepId=5,
                    stepName="调整播放进度",
                    stepDescription="用户拖动进度条调整当前歌曲的播放位置",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[4],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[3, 4, 6, 7],
                ),
                FlowStepNode(
                    stepId=6,
                    stepName="调节播放音量",
                    stepDescription="用户通过音量滑块调节基础音量大小",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[4],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[3, 4, 5, 7],
                ),
                FlowStepNode(
                    stepId=7,
                    stepName="同步更新播放状态",
                    stepDescription="系统实时更新当前播放状态、曲目信息、进度和音量显示",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[4],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[],
                ),
            ],
        ),
        FlowNode(
            flowId=3,
            flowName="本地歌词匹配与显示流程",
            flowDescription="系统根据当前播放歌曲自动匹配本地歌词文件并在界面中同步显示歌词内容",
            featureIds=[7, 11, 18],
            flowSteps=[
                FlowStepNode(
                    stepId=1,
                    stepName="播放歌曲触发歌词匹配",
                    stepDescription="当歌曲开始播放或切换曲目时，系统自动触发歌词匹配流程",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[4, 1],
                    outputBusinessObjectIds=[5],
                    nextStepIds=[2],
                ),
                FlowStepNode(
                    stepId=2,
                    stepName="查找本地歌词文件",
                    stepDescription="系统在本地目录中查找与当前歌曲同名或关联的歌词文件",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[1],
                    outputBusinessObjectIds=[5],
                    nextStepIds=[3, 4],
                ),
                FlowStepNode(
                    stepId=3,
                    stepName="匹配成功并解析歌词",
                    stepDescription="系统解析匹配到的歌词文件内容并生成可同步展示的歌词信息",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[5],
                    outputBusinessObjectIds=[5],
                    nextStepIds=[5],
                ),
                FlowStepNode(
                    stepId=4,
                    stepName="匹配失败并标记无歌词",
                    stepDescription="系统在未找到歌词文件时标记当前歌曲无可用歌词",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[5],
                    outputBusinessObjectIds=[5],
                    nextStepIds=[5],
                ),
                FlowStepNode(
                    stepId=5,
                    stepName="显示并同步歌词",
                    stepDescription="系统在清爽界面中显示歌词内容，并随播放进度同步高亮当前行",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[5, 9],
                    outputBusinessObjectIds=[5],
                    nextStepIds=[],
                ),
            ],
        ),
        FlowNode(
            flowId=4,
            flowName="音效均衡器设置流程",
            flowDescription="用户调整均衡器和音效参数以自定义本地音乐播放效果",
            featureIds=[12, 18],
            flowSteps=[
                FlowStepNode(
                    stepId=1,
                    stepName="打开音效设置面板",
                    stepDescription="用户从播放器界面打开均衡器或音效设置面板",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[9],
                    outputBusinessObjectIds=[6],
                    nextStepIds=[2],
                ),
                FlowStepNode(
                    stepId=2,
                    stepName="加载当前音效配置",
                    stepDescription="系统读取并展示当前启用的均衡器预设和频段参数",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[6],
                    outputBusinessObjectIds=[6],
                    nextStepIds=[3, 4, 5],
                ),
                FlowStepNode(
                    stepId=3,
                    stepName="选择或切换预设",
                    stepDescription="用户选择适合的均衡器预设方案",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[6],
                    outputBusinessObjectIds=[6],
                    nextStepIds=[4, 5],
                ),
                FlowStepNode(
                    stepId=4,
                    stepName="调整频段参数",
                    stepDescription="用户手动调整各频段增益、低音和高音等音效参数",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[6],
                    outputBusinessObjectIds=[6],
                    nextStepIds=[3, 5],
                ),
                FlowStepNode(
                    stepId=5,
                    stepName="应用音效设置",
                    stepDescription="系统将当前音效配置应用到正在播放的音乐",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[6, 4],
                    outputBusinessObjectIds=[6, 4],
                    nextStepIds=[],
                ),
            ],
        ),
        FlowNode(
            flowId=5,
            flowName="歌单自定义管理流程",
            flowDescription="用户创建、编辑、删除自定义歌单，并将本地歌曲加入或移出歌单",
            featureIds=[5, 14, 18],
            flowSteps=[
                FlowStepNode(
                    stepId=1,
                    stepName="新建歌单",
                    stepDescription="用户创建一个新的自定义歌单",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[],
                    outputBusinessObjectIds=[3],
                    nextStepIds=[2],
                ),
                FlowStepNode(
                    stepId=2,
                    stepName="初始化歌单信息",
                    stepDescription="系统生成歌单标识并创建空歌单",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[3],
                    outputBusinessObjectIds=[3],
                    nextStepIds=[3, 4, 5, 6],
                ),
                FlowStepNode(
                    stepId=3,
                    stepName="编辑歌单名称",
                    stepDescription="用户修改歌单名称以便分类管理",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[3],
                    outputBusinessObjectIds=[3],
                    nextStepIds=[4, 5, 6],
                ),
                FlowStepNode(
                    stepId=4,
                    stepName="加入本地歌曲",
                    stepDescription="用户从音乐库中选择歌曲加入当前歌单",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[2, 3],
                    outputBusinessObjectIds=[3],
                    nextStepIds=[3, 5, 6],
                ),
                FlowStepNode(
                    stepId=5,
                    stepName="移除歌单歌曲",
                    stepDescription="用户将已加入的歌曲从歌单中移除",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[3],
                    outputBusinessObjectIds=[3],
                    nextStepIds=[3, 4, 6],
                ),
                FlowStepNode(
                    stepId=6,
                    stepName="删除歌单",
                    stepDescription="用户删除不再需要的自定义歌单",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[3],
                    outputBusinessObjectIds=[],
                    nextStepIds=[],
                ),
            ],
        ),
        FlowNode(
            flowId=6,
            flowName="睡眠定时关闭流程",
            flowDescription="用户设置睡眠定时任务，系统在指定时间后自动停止播放或关闭播放器",
            featureIds=[15, 7],
            flowSteps=[
                FlowStepNode(
                    stepId=1,
                    stepName="设置定时时长或结束时间",
                    stepDescription="用户输入睡眠定时的时长或目标结束时间",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[],
                    outputBusinessObjectIds=[7],
                    nextStepIds=[2],
                ),
                FlowStepNode(
                    stepId=2,
                    stepName="创建并启用定时任务",
                    stepDescription="系统根据用户设置生成睡眠定时任务并开始倒计时",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[7],
                    outputBusinessObjectIds=[7],
                    nextStepIds=[3, 4],
                ),
                FlowStepNode(
                    stepId=3,
                    stepName="查看剩余时间",
                    stepDescription="用户查看当前定时任务的剩余倒计时",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[7],
                    outputBusinessObjectIds=[7],
                    nextStepIds=[4],
                ),
                FlowStepNode(
                    stepId=4,
                    stepName="到时自动停止播放或退出",
                    stepDescription="系统在定时结束后自动停止当前播放或关闭播放器",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[7, 4],
                    outputBusinessObjectIds=[4, 7],
                    nextStepIds=[],
                ),
            ],
        ),
        FlowNode(
            flowId=7,
            flowName="全局快捷键切歌流程",
            flowDescription="用户在系统任意界面通过全局快捷键控制播放器切歌、播放和暂停",
            featureIds=[7, 8, 17, 18],
            flowSteps=[
                FlowStepNode(
                    stepId=1,
                    stepName="配置全局快捷键",
                    stepDescription="用户在设置界面定义上一首、下一首和播放暂停快捷键",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[8],
                    outputBusinessObjectIds=[8],
                    nextStepIds=[2],
                ),
                FlowStepNode(
                    stepId=2,
                    stepName="注册系统全局监听",
                    stepDescription="系统将快捷键配置注册到操作系统，确保任意界面可响应",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[8],
                    outputBusinessObjectIds=[8],
                    nextStepIds=[3, 4, 5],
                ),
                FlowStepNode(
                    stepId=3,
                    stepName="触发上一首快捷键",
                    stepDescription="用户按下上一首全局快捷键",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[8, 4, 3],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[6],
                ),
                FlowStepNode(
                    stepId=4,
                    stepName="触发下一首快捷键",
                    stepDescription="用户按下下一首全局快捷键",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[8, 4, 3],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[6],
                ),
                FlowStepNode(
                    stepId=5,
                    stepName="触发播放暂停快捷键",
                    stepDescription="用户按下播放或暂停全局快捷键",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[8, 4],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[6],
                ),
                FlowStepNode(
                    stepId=6,
                    stepName="更新播放状态并反馈",
                    stepDescription="系统根据快捷键指令切换播放状态并在界面中刷新当前曲目",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[4],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[],
                ),
            ],
        ),
        FlowNode(
            flowId=8,
            flowName="播放器界面轻量化展示流程",
            flowDescription="系统以清爽、纯净、轻量化的方式展示播放器主界面、音乐库、播放列表、歌词和控制区域",
            featureIds=[18, 5, 7, 11, 14, 12, 15, 17],
            flowSteps=[
                FlowStepNode(
                    stepId=1,
                    stepName="打开播放器主界面",
                    stepDescription="用户启动播放器后进入主界面",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[],
                    outputBusinessObjectIds=[9],
                    nextStepIds=[2],
                ),
                FlowStepNode(
                    stepId=2,
                    stepName="加载界面布局与模块",
                    stepDescription="系统按轻量化配置加载音乐库、播放列表、歌词和控制模块",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[9, 2, 3, 5, 4],
                    outputBusinessObjectIds=[9],
                    nextStepIds=[3, 4],
                ),
                FlowStepNode(
                    stepId=3,
                    stepName="浏览并选择功能区域",
                    stepDescription="用户在清爽界面中切换音乐库、歌单、歌词或音效等功能区域",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[9],
                    outputBusinessObjectIds=[9],
                    nextStepIds=[4],
                ),
                FlowStepNode(
                    stepId=4,
                    stepName="保持简洁展示状态",
                    stepDescription="系统持续保持低干扰、少冗余的展示状态，确保界面轻量化体验",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[9],
                    outputBusinessObjectIds=[9],
                    nextStepIds=[],
                ),
            ],
        ),
    ]

    async def main():
        flows_perceptron_result = await flows_perceptron.perceive(
            FlowsPerceptronInput(user_requirements, test_actors, test_features,test_business_objects, test_flows)
        )
    asyncio.run(main())

    result = """
{
  "perceptionDescription": "不需要"
}
"""