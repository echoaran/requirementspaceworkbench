from dataclasses import dataclass
import json
from typing import Dict, List

from backend.core.perceptrons.slot_fillers.prompts.flows_fill_agent import flows_fill_prompt, business_objects_actors_label_prompt
from backend.core.perceptrons.slot_fillers.base_filler import BaseFiller, FillerInput
from backend.schemas import ActorNode, BusinessObjectNode, PerceptionSlot, FeatureNode, FlowNode


# 为流程补充器定义专属的输入类型
@dataclass
class FlowsFillerInput(FillerInput):
    user_requirements: str
    actors: List[ActorNode]
    features: List[FeatureNode]
    business_objects: List[BusinessObjectNode]
    flows: List[FlowNode]
    perception_description: PerceptionSlot

class FlowsFiller(BaseFiller[FlowsFillerInput]):
    async def fill(self, input_data: FlowsFillerInput) -> Dict:
        user_requirements_ = input_data.user_requirements

        features_payload = FeatureNode.schema(
            many=True,
            only=("featureId", "featureName", "featureDescription", "actorIds")
        ).dump(node for node in input_data.features if len(node.childrenIds) == 0)      # 筛选出没有孩子的结点，即叶子结点

        features_ = json.dumps(
            {"features": features_payload},
            ensure_ascii=False,
            indent=2
        )

        perception_description_payload = PerceptionSlot.schema(
            only=("perceptionDescription",)
        ).dump(input_data.perception_description)
        perception_description_ = json.dumps(
            perception_description_payload,
            ensure_ascii=False,
            indent=2,
        )

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
                "flowSteps.nextStepIds",
            ),
        ).dump(input_data.flows)

        flows_ = json.dumps(
            {"flows": flows_payload,},
            ensure_ascii=False,
            indent=2,
        )

        # 第一步，生成补充的流程
        flows_response = await self._llm_handler.call_llm(
            prompt=flows_fill_prompt.replace(
                "{{user_requirements}}",f"{user_requirements_}").replace(
                "{{features}}", f"{features_}").replace(
                "{{flows}}", f"{flows_}").replace(
                "{{perception_description}}", f"{perception_description_}"
            ),
            print_log=False,
        )

        actors_payload = ActorNode.schema(
            many=True,
            only=("actorName", "actorDescription")
        ).dump(input_data.actors)

        actors_ = json.dumps(
            {"actors": actors_payload},
            ensure_ascii=False,
            indent=2
        )

        business_objects_payload = BusinessObjectNode.schema(
            many=True,
            only=(
                "businessObjectId",
                "businessObjectName",
                "businessObjectDescription",
                "businessObjectAttributes",
            ),
        ).dump(input_data.business_objects)

        business_objects_ = json.dumps(
            {"business_objects": business_objects_payload},
            ensure_ascii=False,
            indent=2,
        )

        # 第二步 生成或标记流程相关属性
        response = await self._llm_handler.call_llm(
            prompt=business_objects_actors_label_prompt.replace(
                "{{actors}}", f"{actors_}").replace(
                "{{business_objects}}", f"{business_objects_}").replace(
                "{{flow}}", f"{flows_response}"
            ),
            print_log=False,
        )
        return json.loads(response)

if __name__ == "__main__":
    import asyncio
    from backend.schemas import ActorNode, PerceptionSlot, PerceptionKindType, BusinessObjectAttributeNode, FlowStepNode, FlowStepType

    flows_filler = FlowsFiller()

    user_requirements = "极简纯净本地音乐播放器，不联网、无会员、无广告，只读取电脑本地音乐文件，支持无损格式 Flac/WAV/MP3 播放，自带歌词本地匹配、音效均衡器、歌单自定义、睡眠定时关闭、全局快捷键切歌，界面清爽轻量化，替代臃肿的主流音乐播放器。"
    test_features: List[FeatureNode] = [
        FeatureNode(
            featureId=1,
            featureName="极简纯净本地音乐播放器",
            featureDescription="系统用于在电脑本地离线播放音乐文件，支持无损与常见音频格式播放，并提供歌词匹配、音效均衡、歌单管理、睡眠定时、全局快捷键和轻量化界面等功能，旨在替代臃肿的主流音乐播放器。",
            actorIds=[1, 2, 3, 4, 5, 6, 7],
            childrenIds=[2, 6, 10, 14, 18, 22, 26]
        ),
        FeatureNode(
            featureId=2,
            featureName="本地音乐播放管理",
            featureDescription="支持读取电脑本地音乐文件并进行播放控制、进度调整和格式播放管理。",
            actorIds=[1],
            childrenIds=[3, 4, 5]
        ),
        FeatureNode(
            featureId=3,
            featureName="扫描与导入本地音乐",
            featureDescription="支持从电脑本地读取、扫描和导入音乐文件，作为播放器的媒体来源。",
            actorIds=[1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=4,
            featureName="播放控制",
            featureDescription="支持播放、暂停、上一首、下一首和播放进度调整等基础播放操作。",
            actorIds=[1, 6],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=5,
            featureName="音频格式播放",
            featureDescription="支持播放本地无损及常见音频格式文件，包括 Flac、WAV 和 MP3。",
            actorIds=[1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=6,
            featureName="歌单自定义管理",
            featureDescription="支持用户按个人喜好创建、编辑和维护本地音乐歌单。",
            actorIds=[2, 1],
            childrenIds=[7, 8, 9]
        ),
        FeatureNode(
            featureId=7,
            featureName="新建与删除歌单",
            featureDescription="支持用户创建新的歌单并删除不再需要的歌单。",
            actorIds=[2],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=8,
            featureName="添加或移除歌曲",
            featureDescription="支持用户将本地歌曲添加到歌单中或从歌单中移除。",
            actorIds=[2, 1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=9,
            featureName="歌单排序与自定义内容",
            featureDescription="支持用户调整歌单内歌曲顺序，并按个人偏好自定义歌单内容。",
            actorIds=[2],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=10,
            featureName="歌词匹配与显示",
            featureDescription="支持本地歌曲歌词自动匹配、显示与同步管理。",
            actorIds=[4],
            childrenIds=[11, 12, 13]
        ),
        FeatureNode(
            featureId=11,
            featureName="本地歌词自动匹配",
            featureDescription="支持根据本地歌曲自动匹配对应歌词文件或歌词内容。",
            actorIds=[4],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=12,
            featureName="歌词显示与同步调整",
            featureDescription="支持在播放界面显示歌词，并调整歌词同步效果以匹配播放进度。",
            actorIds=[4, 1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=13,
            featureName="歌词关联管理",
            featureDescription="支持用户管理歌词与歌曲的关联结果，便于维护匹配准确性。",
            actorIds=[4],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=14,
            featureName="音效与均衡器设置",
            featureDescription="支持用户根据听感调整音效参数与均衡器配置。",
            actorIds=[3],
            childrenIds=[15, 16, 17]
        ),
        FeatureNode(
            featureId=15,
            featureName="均衡器调节",
            featureDescription="支持用户调整均衡器各频段参数，以优化不同音乐风格的听感。",
            actorIds=[3],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=16,
            featureName="音效参数配置",
            featureDescription="支持用户配置音效相关参数，并保存个人偏好设置。",
            actorIds=[3],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=17,
            featureName="预设音效切换",
            featureDescription="支持用户切换系统提供的预设音效方案。",
            actorIds=[3],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=18,
            featureName="睡眠定时关闭",
            featureDescription="支持设置定时关闭播放器，在指定时间自动停止播放并退出或关闭程序。",
            actorIds=[5],
            childrenIds=[19, 20, 21]
        ),
        FeatureNode(
            featureId=19,
            featureName="设置定时关闭时间",
            featureDescription="支持用户设置播放器在指定时间后自动关闭。",
            actorIds=[5],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=20,
            featureName="取消定时与查看倒计时",
            featureDescription="支持用户取消已设置的定时关闭，并查看剩余倒计时。",
            actorIds=[5],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=21,
            featureName="管理播放结束行为",
            featureDescription="支持用户配置定时结束后播放器的处理方式，如停止播放或关闭程序。",
            actorIds=[5],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=22,
            featureName="全局快捷键控制",
            featureDescription="支持通过系统全局快捷键快速控制音乐播放。",
            actorIds=[6],
            childrenIds=[23, 24, 25]
        ),
        FeatureNode(
            featureId=23,
            featureName="切歌快捷键设置",
            featureDescription="支持用户设置全局切歌快捷键，以便快速控制播放。",
            actorIds=[6],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=24,
            featureName="快捷键播放控制",
            featureDescription="支持通过全局快捷键执行播放、暂停、上一首和下一首操作。",
            actorIds=[6, 1],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=25,
            featureName="快速调节播放状态",
            featureDescription="支持通过快捷键快速调整当前播放状态，提升操作效率。",
            actorIds=[6],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=26,
            featureName="清爽轻量化界面设置",
            featureDescription="支持配置播放器界面风格与显示方式，保持界面简洁、轻量和低干扰。",
            actorIds=[7],
            childrenIds=[27, 28, 29]
        ),
        FeatureNode(
            featureId=27,
            featureName="界面显示样式调整",
            featureDescription="支持用户调整界面显示样式，使播放器保持清爽直观。",
            actorIds=[7],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=28,

            featureName="轻量化布局切换",
            featureDescription="支持用户切换轻量化布局，减少不必要的视觉元素与操作干扰。",
            actorIds=[7],
            childrenIds=[]
        ),
        FeatureNode(
            featureId=29,
            featureName="视觉风格与外观偏好管理",
            featureDescription="支持用户配置播放器视觉风格，满足长期使用中的外观偏好。",
            actorIds=[7],
            childrenIds=[]
        )
    ]
    test_actors = [
        ActorNode(
            actorId=1,
            actorName="本地音乐听众",
            actorDescription="本地音乐听众是指在需要播放和聆听电脑本地音乐文件的场景下，与音乐播放器发生交互，并可执行导入或扫描本地音乐、播放暂停、切换上一首下一首、调整播放进度、管理播放列表和选择音频格式进行播放等操作的用户角色。"
        ),
        ActorNode(
            actorId=2,
            actorName="歌单管理者",
            actorDescription="歌单管理者是指在需要按个人喜好整理和归类本地音乐的场景下，与歌单管理功能发生交互，并可执行新建歌单、编辑歌单、添加或移除歌曲、排序歌曲、删除歌单和自定义歌单内容等操作的用户角色。"
        ),
        ActorNode(
            actorId=3,
            actorName="音效调节者",
            actorDescription="音效调节者是指在需要根据听感优化音乐播放效果的场景下，与音效设置功能发生交互，并可执行调整均衡器、配置音效参数、切换预设音效和保存个人音效偏好等操作的用户角色。"
        ),
        ActorNode(
            actorId=4,
            actorName="歌词匹配者",
            actorDescription="歌词匹配者是指在需要查看本地歌曲对应歌词的场景下，与歌词匹配功能发生交互，并可执行本地歌词自动匹配、查看歌词显示、调整歌词同步效果和管理歌词关联结果等操作的用户角色。"
        ),
        ActorNode(
            actorId=5,
            actorName="睡眠定时设置者",
            actorDescription="睡眠定时设置者是指在需要限定音乐播放时长并在指定时间自动关闭播放器的场景下，与睡眠定时功能发生交互，并可执行设置定时关闭时间、取消定时、查看倒计时和管理播放结束行为等操作的用户角色。"
        ),
        ActorNode(
            actorId=6,
            actorName="快捷键控制者",
            actorDescription="快捷键控制者是指在需要通过全局快捷键快速控制播放的场景下，与全局快捷键功能发生交互，并可执行设置切歌快捷键、使用快捷键播放暂停、上一首下一首切换和快速调节播放控制等操作的用户角色。"
        ),
        ActorNode(
            actorId=7,
            actorName="界面偏好设置者",
            actorDescription="界面偏好设置者是指在需要让播放器保持清爽、轻量和低干扰使用体验的场景下，与界面设置功能发生交互，并可执行调整界面显示样式、切换轻量化布局、配置视觉风格和管理播放器外观偏好的用户角色。"
        ),
    ]
    test_business_objects = [
        BusinessObjectNode(
            businessObjectId=1,
            businessObjectName="本地音乐文件",
            businessObjectDescription="播放器从电脑本地扫描、识别并读取的音频文件对象，作为播放、导入、歌词匹配和歌单管理的基础数据来源。",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=1,
                    businessObjectAttributeName="music_id",
                    businessObjectAttributeDescription="本地音乐文件唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="M-001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=2,
                    businessObjectAttributeName="file_path",
                    businessObjectAttributeDescription="音乐文件在本地磁盘中的完整路径",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample=r"D:\Music\周杰伦\晴天.flac",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=3,
                    businessObjectAttributeName="file_name",
                    businessObjectAttributeDescription="音乐文件名称",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="晴天.flac",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=4,
                    businessObjectAttributeName="audio_format",
                    businessObjectAttributeDescription="音频格式类型",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="flac",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=5,
                    businessObjectAttributeName="duration_seconds",
                    businessObjectAttributeDescription="音频时长，单位为秒",
                    businessObjectAttributeType="integer",
                    businessObjectAttributeExample="269",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=6,
                    businessObjectAttributeName="title",
                    businessObjectAttributeDescription="歌曲标题",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="晴天",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=7,
                    businessObjectAttributeName="artist",
                    businessObjectAttributeDescription="歌曲歌手名称",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="周杰伦",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=8,
                    businessObjectAttributeName="album",
                    businessObjectAttributeDescription="所属专辑名称",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="叶惠美",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=9,
                    businessObjectAttributeName="is_available",
                    businessObjectAttributeDescription="文件当前是否可被读取播放",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
            ],
        ),
        BusinessObjectNode(
            businessObjectId=2,
            businessObjectName="播放会话",
            businessObjectDescription="播放器当前的播放上下文，用于记录正在播放的歌曲、播放状态、播放进度和切换行为。",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=10,
                    businessObjectAttributeName="playback_session_id",
                    businessObjectAttributeDescription="播放会话唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="PS-001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=11,
                    businessObjectAttributeName="current_music_id",
                    businessObjectAttributeDescription="当前播放的音乐文件标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="M-001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=12,
                    businessObjectAttributeName="play_status",
                    businessObjectAttributeDescription="当前播放状态，如播放中、暂停、停止",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="playing",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=13,
                    businessObjectAttributeName="progress_seconds",
                    businessObjectAttributeDescription="当前播放进度秒数",
                    businessObjectAttributeType="integer",
                    businessObjectAttributeExample="128",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=14,
                    businessObjectAttributeName="volume",
                    businessObjectAttributeDescription="当前音量值",
                    businessObjectAttributeType="integer",
                    businessObjectAttributeExample="70",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=15,
                    businessObjectAttributeName="play_source",
                    businessObjectAttributeDescription="当前播放来源，如音乐库或歌单",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="playlist",
                ),
            ],
        ),
        BusinessObjectNode(
            businessObjectId=3,
            businessObjectName="歌单",
            businessObjectDescription="用户自定义维护的歌曲集合，用于按个人喜好整理、排序和播放本地音乐。",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=16,
                    businessObjectAttributeName="playlist_id",
                    businessObjectAttributeDescription="歌单唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="PL-001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=17,
                    businessObjectAttributeName="playlist_name",
                    businessObjectAttributeDescription="歌单名称",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="深夜循环",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=18,
                    businessObjectAttributeName="music_ids",
                    businessObjectAttributeDescription="歌单内歌曲标识列表",
                    businessObjectAttributeType="array[string]",
                    businessObjectAttributeExample='["M-001", "M-003", "M-008"]',
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=19,
                    businessObjectAttributeName="song_count",
                    businessObjectAttributeDescription="歌单内歌曲数量",
                    businessObjectAttributeType="integer",
                    businessObjectAttributeExample="3",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=20,
                    businessObjectAttributeName="custom_order_enabled",
                    businessObjectAttributeDescription="是否启用自定义排序",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
            ],
        ),
        BusinessObjectNode(
            businessObjectId=4,
            businessObjectName="歌词关联",
            businessObjectDescription="歌曲与本地歌词文件之间的匹配与同步数据，用于歌词显示、偏移调整和关联维护。",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=21,
                    businessObjectAttributeName="lyric_link_id",
                    businessObjectAttributeDescription="歌词关联唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="L-001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=22,
                    businessObjectAttributeName="music_id",
                    businessObjectAttributeDescription="关联的歌曲标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="M-001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=23,
                    businessObjectAttributeName="lyric_file_path",
                    businessObjectAttributeDescription="本地歌词文件路径",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample=r"D:\Lyrics\晴天.lrc",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=24,
                    businessObjectAttributeName="match_status",
                    businessObjectAttributeDescription="歌词匹配状态，如已匹配、未匹配、手动关联",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="matched",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=25,
                    businessObjectAttributeName="sync_offset_ms",
                    businessObjectAttributeDescription="歌词同步偏移毫秒值",
                    businessObjectAttributeType="integer",
                    businessObjectAttributeExample="250",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=26,
                    businessObjectAttributeName="display_enabled",
                    businessObjectAttributeDescription="播放界面是否启用歌词显示",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
            ],
        ),
        BusinessObjectNode(
            businessObjectId=5,
            businessObjectName="音效配置",
            businessObjectDescription="用户针对播放器设置的均衡器和音效参数配置，可切换预设并保存个人偏好。",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=27,
                    businessObjectAttributeName="effect_config_id",
                    businessObjectAttributeDescription="音效配置唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="EQ-001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=28,
                    businessObjectAttributeName="preset_name",
                    businessObjectAttributeDescription="当前使用的预设名称",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="流行",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=29,
                    businessObjectAttributeName="band_settings",
                    businessObjectAttributeDescription="均衡器各频段参数集合",
                    businessObjectAttributeType="object",
                    businessObjectAttributeExample='{"60Hz":"+3","230Hz":"+1","910Hz":"0","4kHz":"+2","14kHz":"+4"}',
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=30,
                    businessObjectAttributeName="effect_enabled",
                    businessObjectAttributeDescription="是否启用音效处理",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=31,
                    businessObjectAttributeName="user_saved",
                    businessObjectAttributeDescription="当前配置是否已保存为用户偏好",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
            ],
        ),
        BusinessObjectNode(
            businessObjectId=6,
            businessObjectName="睡眠定时任务",
            businessObjectDescription="用户设置的播放定时结束控制数据，用于记录倒计时、结束行为和启用状态。",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=32,
                    businessObjectAttributeName="sleep_timer_id",
                    businessObjectAttributeDescription="睡眠定时任务唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="ST-001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=33,
                    businessObjectAttributeName="remaining_seconds",
                    businessObjectAttributeDescription="剩余倒计时秒数",
                    businessObjectAttributeType="integer",
                    businessObjectAttributeExample="1800",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=34,
                    businessObjectAttributeName="target_action",
                    businessObjectAttributeDescription="定时结束后执行的行为",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="close_app",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=35,
                    businessObjectAttributeName="is_active",
                    businessObjectAttributeDescription="定时任务是否处于启用状态",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=36,
                    businessObjectAttributeName="start_time",
                    businessObjectAttributeDescription="定时任务开始时间",
                    businessObjectAttributeType="datetime",
                    businessObjectAttributeExample="2026-05-20 23:30:00",
                ),
            ],
        ),
        BusinessObjectNode(
            businessObjectId=7,
            businessObjectName="快捷键配置",
            businessObjectDescription="播放器全局快捷键的映射和启用状态配置，用于快速控制播放和切歌。",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=37,
                    businessObjectAttributeName="shortcut_config_id",
                    businessObjectAttributeDescription="快捷键配置唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="SC-001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=38,
                    businessObjectAttributeName="play_pause_key",
                    businessObjectAttributeDescription="播放暂停快捷键组合",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="Ctrl+Alt+Space",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=39,
                    businessObjectAttributeName="previous_key",
                    businessObjectAttributeDescription="上一首快捷键组合",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="Ctrl+Alt+Left",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=40,
                    businessObjectAttributeName="next_key",
                    businessObjectAttributeDescription="下一首快捷键组合",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="Ctrl+Alt+Right",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=41,
                    businessObjectAttributeName="enabled",
                    businessObjectAttributeDescription="全局快捷键是否启用",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="true",
                ),
            ],
        ),
        BusinessObjectNode(
            businessObjectId=8,
            businessObjectName="界面偏好设置",
            businessObjectDescription="用户针对播放器界面样式、轻量布局和视觉风格的长期偏好配置。",
            businessObjectAttributes=[
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=42,
                    businessObjectAttributeName="ui_preference_id",
                    businessObjectAttributeDescription="界面偏好设置唯一标识",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="UI-001",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=43,
                    businessObjectAttributeName="theme_style",
                    businessObjectAttributeDescription="界面主题风格",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="纯净浅色",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=44,
                    businessObjectAttributeName="layout_mode",
                    businessObjectAttributeDescription="界面布局模式",
                    businessObjectAttributeType="string",
                    businessObjectAttributeExample="轻量模式",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=45,
                    businessObjectAttributeName="show_extra_panels",
                    businessObjectAttributeDescription="是否显示额外信息面板",
                    businessObjectAttributeType="bool",
                    businessObjectAttributeExample="false",
                ),
                BusinessObjectAttributeNode(
                    businessObjectAttributeId=46,
                    businessObjectAttributeName="font_scale",
                    businessObjectAttributeDescription="界面字体缩放比例",
                    businessObjectAttributeType="decimal",
                    businessObjectAttributeExample="1.0",
                ),
            ],
        ),
    ]
    test_flows = [
        FlowNode(
            flowId=1,
            flowName="本地音乐导入与播放流程",
            flowDescription="用户扫描或导入电脑本地音乐文件，系统识别可播放音频格式并加入音乐库，用户选择歌曲后进行播放控制。",
            featureIds=[1, 2, 3],
            flowSteps=[
                FlowStepNode(
                    stepId=1,
                    stepName="选择音乐导入入口",
                    stepDescription="用户选择扫描本地目录或手动导入音乐文件。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[],
                    outputBusinessObjectIds=[1],
                    nextStepIds=[2],
                ),
                FlowStepNode(
                    stepId=2,
                    stepName="读取本地音乐文件",
                    stepDescription="系统读取用户指定目录或文件，并提取文件路径、文件名、格式和时长等基础信息。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[1],
                    outputBusinessObjectIds=[1],
                    nextStepIds=[3],
                ),
                FlowStepNode(
                    stepId=3,
                    stepName="判断音频格式是否支持",
                    stepDescription="系统判断导入文件是否属于支持的音频格式，如 MP3、WAV 或 Flac。",
                    stepType=FlowStepType.JUDGMENT,
                    actorIds=[],
                    inputBusinessObjectIds=[1],
                    outputBusinessObjectIds=[],
                    nextStepIds=[4, 5],
                ),
                FlowStepNode(
                    stepId=4,
                    stepName="加入音乐库",
                    stepDescription="系统将支持播放的本地音乐文件写入音乐库。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[1],
                    outputBusinessObjectIds=[2],
                    nextStepIds=[6],
                ),
                FlowStepNode(
                    stepId=5,
                    stepName="忽略不支持文件",
                    stepDescription="系统忽略不支持的音频文件，并结束该文件的导入处理。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[1],
                    outputBusinessObjectIds=[],
                    nextStepIds=[],
                ),
                FlowStepNode(
                    stepId=6,
                    stepName="选择歌曲播放",
                    stepDescription="用户从音乐库中选择一首歌曲进行播放。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1],
                    inputBusinessObjectIds=[2],
                    outputBusinessObjectIds=[3],
                    nextStepIds=[7],
                ),
                FlowStepNode(
                    stepId=7,
                    stepName="执行播放",
                    stepDescription="系统加载用户选择的音乐文件并创建播放会话。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[1, 3],
                    outputBusinessObjectIds=[3],
                    nextStepIds=[8],
                ),
                FlowStepNode(
                    stepId=8,
                    stepName="控制播放状态",
                    stepDescription="用户执行播放、暂停、上一首、下一首或调整播放进度等操作。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[1, 6],
                    inputBusinessObjectIds=[3],
                    outputBusinessObjectIds=[3],
                    nextStepIds=[9],
                ),
                FlowStepNode(
                    stepId=9,
                    stepName="更新播放会话",
                    stepDescription="系统根据用户操作更新当前歌曲、播放状态和播放进度。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[3],
                    outputBusinessObjectIds=[3],
                    nextStepIds=[],
                ),
            ],
        ),
        FlowNode(
            flowId=2,
            flowName="歌单管理流程",
            flowDescription="用户创建或删除歌单，将本地歌曲添加到歌单或从歌单移除，并按照个人偏好调整歌曲顺序。",
            featureIds=[4, 5, 6],
            flowSteps=[
                FlowStepNode(
                    stepId=10,
                    stepName="创建或选择歌单",
                    stepDescription="用户创建新的歌单，或选择已有歌单进行维护。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[2],
                    inputBusinessObjectIds=[4],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[11],
                ),
                FlowStepNode(
                    stepId=11,
                    stepName="保存歌单基础信息",
                    stepDescription="系统保存歌单名称、歌单编号和初始歌曲集合。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[4],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[12],
                ),
                FlowStepNode(
                    stepId=12,
                    stepName="选择歌单操作类型",
                    stepDescription="用户选择添加歌曲、移除歌曲、调整排序或删除歌单。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[2, 1],
                    inputBusinessObjectIds=[2, 4],
                    outputBusinessObjectIds=[],
                    nextStepIds=[13],
                ),
                FlowStepNode(
                    stepId=13,
                    stepName="判断操作类型",
                    stepDescription="系统判断用户当前选择的歌单维护操作。",
                    stepType=FlowStepType.JUDGMENT,
                    actorIds=[],
                    inputBusinessObjectIds=[4],
                    outputBusinessObjectIds=[],
                    nextStepIds=[14, 15, 16, 17],
                ),
                FlowStepNode(
                    stepId=14,
                    stepName="添加歌曲到歌单",
                    stepDescription="系统将用户从音乐库中选择的歌曲加入目标歌单。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[1, 2, 4],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[18],
                ),
                FlowStepNode(
                    stepId=15,
                    stepName="从歌单移除歌曲",
                    stepDescription="系统将用户指定的歌曲从目标歌单中移除。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[4],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[18],
                ),
                FlowStepNode(
                    stepId=16,
                    stepName="调整歌曲顺序",
                    stepDescription="系统根据用户指定的顺序更新歌单内歌曲排序。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[4],
                    outputBusinessObjectIds=[4],
                    nextStepIds=[18],
                ),
                FlowStepNode(
                    stepId=17,
                    stepName="删除歌单",
                    stepDescription="系统删除用户指定的不再需要的歌单。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[4],
                    outputBusinessObjectIds=[],
                    nextStepIds=[],
                ),
                FlowStepNode(
                    stepId=18,
                    stepName="保存歌单变更",
                    stepDescription="系统保存歌单内容和排序变更，供后续播放和管理使用。",
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
            flowName="歌词匹配与同步流程",
            flowDescription="系统根据本地歌曲自动匹配歌词，用户查看歌词显示效果，并可调整同步偏移或管理歌词关联关系。",
            featureIds=[7, 8, 9],
            flowSteps=[
                FlowStepNode(
                    stepId=19,
                    stepName="选择需要匹配歌词的歌曲",
                    stepDescription="用户选择一首本地歌曲，触发歌词匹配或歌词显示。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[4, 1],
                    inputBusinessObjectIds=[1],
                    outputBusinessObjectIds=[],
                    nextStepIds=[20],
                ),
                FlowStepNode(
                    stepId=20,
                    stepName="自动查找歌词",
                    stepDescription="系统根据歌曲文件名、歌曲信息或本地歌词目录自动查找对应歌词文件。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[1],
                    outputBusinessObjectIds=[5],
                    nextStepIds=[21],
                ),
                FlowStepNode(
                    stepId=21,
                    stepName="判断歌词是否匹配成功",
                    stepDescription="系统判断是否找到可用歌词，并确认歌词是否可与当前歌曲建立关联。",
                    stepType=FlowStepType.JUDGMENT,
                    actorIds=[],
                    inputBusinessObjectIds=[1, 5],
                    outputBusinessObjectIds=[],
                    nextStepIds=[22, 23],
                ),
                FlowStepNode(
                    stepId=22,
                    stepName="建立歌词关联",
                    stepDescription="系统将匹配到的歌词与当前歌曲建立关联关系。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[1, 5],
                    outputBusinessObjectIds=[6],
                    nextStepIds=[24],
                ),
                FlowStepNode(
                    stepId=23,
                    stepName="手动管理歌词关联",
                    stepDescription="用户手动选择歌词文件或调整歌曲与歌词的关联结果。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[4],
                    inputBusinessObjectIds=[1, 5, 6],
                    outputBusinessObjectIds=[6],
                    nextStepIds=[24],
                ),
                FlowStepNode(
                    stepId=24,
                    stepName="显示歌词",
                    stepDescription="系统在播放界面中按照当前播放进度显示歌词。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[3, 5, 6],
                    outputBusinessObjectIds=[5],
                    nextStepIds=[25],
                ),
                FlowStepNode(
                    stepId=25,
                    stepName="调整歌词同步效果",
                    stepDescription="用户根据播放效果调整歌词时间偏移，使歌词与音乐播放进度一致。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[4, 1],
                    inputBusinessObjectIds=[5],
                    outputBusinessObjectIds=[5],
                    nextStepIds=[26],
                ),
                FlowStepNode(
                    stepId=26,
                    stepName="保存歌词同步设置",
                    stepDescription="系统保存歌词时间偏移和关联结果，供后续播放时复用。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[5, 6],
                    outputBusinessObjectIds=[5, 6],
                    nextStepIds=[],
                ),
            ],
        ),
        FlowNode(
            flowId=4,
            flowName="音效调节流程",
            flowDescription="用户通过预设音效、均衡器和音效参数配置优化音乐播放效果，系统保存并应用个人音效偏好。",
            featureIds=[10, 11, 12],
            flowSteps=[
                FlowStepNode(
                    stepId=27,
                    stepName="打开音效设置",
                    stepDescription="用户进入音效设置界面，准备调整播放效果。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[3],
                    inputBusinessObjectIds=[],
                    outputBusinessObjectIds=[],
                    nextStepIds=[28],
                ),
                FlowStepNode(
                    stepId=28,
                    stepName="选择音效调节方式",
                    stepDescription="用户选择切换预设音效、手动调整均衡器或配置其他音效参数。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[3],
                    inputBusinessObjectIds=[7],
                    outputBusinessObjectIds=[],
                    nextStepIds=[29],
                ),
                FlowStepNode(
                    stepId=29,
                    stepName="判断音效调节方式",
                    stepDescription="系统判断用户选择的是预设音效、均衡器调整还是参数配置。",
                    stepType=FlowStepType.JUDGMENT,
                    actorIds=[],
                    inputBusinessObjectIds=[7],
                    outputBusinessObjectIds=[],
                    nextStepIds=[30, 31, 32],
                ),
                FlowStepNode(
                    stepId=30,
                    stepName="切换预设音效",
                    stepDescription="系统根据用户选择切换到对应的预设音效方案。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[7],
                    outputBusinessObjectIds=[7],
                    nextStepIds=[33],
                ),
                FlowStepNode(
                    stepId=31,
                    stepName="调整均衡器参数",
                    stepDescription="用户调整均衡器各频段参数，形成新的均衡器设置。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[3],
                    inputBusinessObjectIds=[7],
                    outputBusinessObjectIds=[7],
                    nextStepIds=[33],
                ),
                FlowStepNode(
                    stepId=32,
                    stepName="配置音效参数",
                    stepDescription="用户配置其他音效参数，并决定是否保存为个人偏好。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[3],
                    inputBusinessObjectIds=[7],
                    outputBusinessObjectIds=[7],
                    nextStepIds=[33],
                ),
                FlowStepNode(
                    stepId=33,
                    stepName="应用音效配置",
                    stepDescription="系统将新的音效配置应用到当前播放会话。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[3, 7],
                    outputBusinessObjectIds=[3],
                    nextStepIds=[34],
                ),
                FlowStepNode(
                    stepId=34,
                    stepName="保存音效偏好",
                    stepDescription="系统保存用户配置的预设音效、均衡器参数和个人音效偏好。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[7],
                    outputBusinessObjectIds=[7],
                    nextStepIds=[],
                ),
            ],
        ),
        FlowNode(
            flowId=5,
            flowName="睡眠定时关闭流程",
            flowDescription="用户设置定时关闭时间和播放结束行为，系统执行倒计时并在到期后停止播放或关闭程序。",
            featureIds=[13, 14, 15],
            flowSteps=[
                FlowStepNode(
                    stepId=35,
                    stepName="设置定时关闭时间",
                    stepDescription="用户输入定时关闭时长或指定关闭时间。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[5],
                    inputBusinessObjectIds=[],
                    outputBusinessObjectIds=[8],
                    nextStepIds=[36],
                ),
                FlowStepNode(
                    stepId=36,
                    stepName="设置播放结束行为",
                    stepDescription="用户选择倒计时结束后的处理方式，如停止播放或关闭程序。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[5],
                    inputBusinessObjectIds=[8],
                    outputBusinessObjectIds=[8],
                    nextStepIds=[37],
                ),
                FlowStepNode(
                    stepId=37,
                    stepName="启动倒计时",
                    stepDescription="系统保存定时关闭设置并启动倒计时。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[8],
                    outputBusinessObjectIds=[8],
                    nextStepIds=[38],
                ),
                FlowStepNode(
                    stepId=38,
                    stepName="查看或取消倒计时",
                    stepDescription="用户查看剩余倒计时，或取消已经设置的定时关闭。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[5],
                    inputBusinessObjectIds=[8],
                    outputBusinessObjectIds=[8],
                    nextStepIds=[39],
                ),
                FlowStepNode(
                    stepId=39,
                    stepName="判断定时状态",
                    stepDescription="系统判断定时任务是已取消、继续倒计时还是已经到期。",
                    stepType=FlowStepType.JUDGMENT,
                    actorIds=[],
                    inputBusinessObjectIds=[8],
                    outputBusinessObjectIds=[],
                    nextStepIds=[40, 41, 42],
                ),
                FlowStepNode(
                    stepId=40,
                    stepName="取消定时任务",
                    stepDescription="系统取消当前睡眠定时任务，并清除倒计时状态。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[8],
                    outputBusinessObjectIds=[8],
                    nextStepIds=[],
                ),
                FlowStepNode(
                    stepId=41,
                    stepName="继续倒计时",
                    stepDescription="系统继续维护倒计时并更新剩余时间。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[8],
                    outputBusinessObjectIds=[8],
                    nextStepIds=[38],
                ),
                FlowStepNode(
                    stepId=42,
                    stepName="执行结束行为",
                    stepDescription="系统在倒计时结束后按照用户配置停止播放或关闭程序。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[3, 8],
                    outputBusinessObjectIds=[3, 8],
                    nextStepIds=[],
                ),
            ],
        ),
        FlowNode(
            flowId=6,
            flowName="全局快捷键控制流程",
            flowDescription="用户配置全局快捷键，系统校验并保存快捷键绑定，用户通过快捷键快速执行播放控制操作。",
            featureIds=[16, 17, 18],
            flowSteps=[
                FlowStepNode(
                    stepId=43,
                    stepName="进入快捷键设置",
                    stepDescription="用户打开快捷键设置入口，准备配置播放控制快捷键。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[6],
                    inputBusinessObjectIds=[],
                    outputBusinessObjectIds=[],
                    nextStepIds=[44],
                ),
                FlowStepNode(
                    stepId=44,
                    stepName="配置快捷键组合",
                    stepDescription="用户为播放、暂停、上一首和下一首等命令设置快捷键组合。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[6],
                    inputBusinessObjectIds=[],
                    outputBusinessObjectIds=[9],
                    nextStepIds=[45],
                ),
                FlowStepNode(
                    stepId=45,
                    stepName="校验快捷键冲突",
                    stepDescription="系统校验快捷键组合是否为空、重复或与已有快捷键冲突。",
                    stepType=FlowStepType.JUDGMENT,
                    actorIds=[],
                    inputBusinessObjectIds=[9],
                    outputBusinessObjectIds=[],
                    nextStepIds=[46, 47],
                ),
                FlowStepNode(
                    stepId=46,
                    stepName="提示重新设置",
                    stepDescription="系统提示快捷键不可用，要求用户重新设置快捷键组合。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[9],
                    outputBusinessObjectIds=[],
                    nextStepIds=[44],
                ),
                FlowStepNode(
                    stepId=47,
                    stepName="保存快捷键配置",
                    stepDescription="系统保存有效的快捷键配置并启用全局快捷键监听。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[9],
                    outputBusinessObjectIds=[9],
                    nextStepIds=[48],
                ),
                FlowStepNode(
                    stepId=48,
                    stepName="触发快捷键",
                    stepDescription="用户在任意场景下按下已配置的全局快捷键。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[6, 1],
                    inputBusinessObjectIds=[9],
                    outputBusinessObjectIds=[],
                    nextStepIds=[49],
                ),
                FlowStepNode(
                    stepId=49,
                    stepName="识别快捷键命令",
                    stepDescription="系统根据快捷键配置识别用户触发的播放控制命令。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[9],
                    outputBusinessObjectIds=[],
                    nextStepIds=[50],
                ),
                FlowStepNode(
                    stepId=50,
                    stepName="执行播放控制",
                    stepDescription="系统执行对应的播放、暂停、上一首、下一首或快速调节播放状态操作。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[3, 9],
                    outputBusinessObjectIds=[3],
                    nextStepIds=[],
                ),
            ],
        ),
        FlowNode(
            flowId=7,
            flowName="界面偏好设置流程",
            flowDescription="用户调整播放器界面显示样式、轻量化布局和视觉风格，系统保存并应用界面偏好。",
            featureIds=[19, 20, 21],
            flowSteps=[
                FlowStepNode(
                    stepId=51,
                    stepName="进入界面设置",
                    stepDescription="用户进入播放器界面设置入口。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[7],
                    inputBusinessObjectIds=[],
                    outputBusinessObjectIds=[],
                    nextStepIds=[52],
                ),
                FlowStepNode(
                    stepId=52,
                    stepName="调整界面显示样式",
                    stepDescription="用户调整界面显示样式、视觉风格或是否显示额外视觉元素。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[7],
                    inputBusinessObjectIds=[10],
                    outputBusinessObjectIds=[10],
                    nextStepIds=[53],
                ),
                FlowStepNode(
                    stepId=53,
                    stepName="选择布局模式",
                    stepDescription="用户选择标准布局或轻量化布局，以减少操作干扰。",
                    stepType=FlowStepType.ACTOR_ACTION,
                    actorIds=[7],
                    inputBusinessObjectIds=[10],
                    outputBusinessObjectIds=[10],
                    nextStepIds=[54],
                ),
                FlowStepNode(
                    stepId=54,
                    stepName="应用界面偏好",
                    stepDescription="系统根据用户选择立即调整界面布局、视觉风格和显示元素。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[10],
                    outputBusinessObjectIds=[10],
                    nextStepIds=[55],
                ),
                FlowStepNode(
                    stepId=55,
                    stepName="保存界面设置",
                    stepDescription="系统保存用户界面偏好，供后续启动播放器时自动加载。",
                    stepType=FlowStepType.SYSTEM_ACTION,
                    actorIds=[],
                    inputBusinessObjectIds=[10],
                    outputBusinessObjectIds=[10],
                    nextStepIds=[],
                ),
            ],
        ),
    ]
    test_perception_slot = PerceptionSlot(
        perceptionSlotId = 1,
        perceptionKind = PerceptionKindType.FLOW,
        perceptionDescription = "需要补充“播放器启动与偏好恢复流程”。原因是当前已有流程覆盖了导入播放、歌单管理、歌词、音效、睡眠定时、全局快捷键和界面偏好的配置与使用，但缺少一个从“启动应用”到“恢复用户习惯状态”的整体运行流程：例如读取已保存的音乐库、音效设置、界面布局、快捷键绑定、歌词同步偏移以及上次播放状态（如是否继续上次播放、默认打开哪个歌单/页面）等。对一个强调极简、清爽、替代主流播放器的本地播放器来说，这种“启动即就绪”的能力是核心体验的一部分，仅靠单独的设置流程无法体现其在应用启动时如何被应用。补充方式是新增一个“播放器启动与会话恢复流程”，不引入新 feature，而是关联已有音效、界面偏好、快捷键、歌词匹配、音乐导入等相关 feature：步骤可包括（1）启动应用并加载基础配置；（2）读取已保存音乐库索引（如不存在则提示用户扫描本地音乐）；（3）加载用户界面偏好和布局（标准/轻量、视觉风格）；（4）加载音效配置并应用到默认输出；（5）注册全局快捷键；（6）恢复歌词关联与同步偏移；（7）根据用户设置决定是否自动恢复上次播放会话（歌曲、播放位置或仅停留在暂停状态）。通过该启动流程，将零散的设置/控制能力在应用生命周期入口处整合起来，确保系统行为与“极简纯净”“开箱即用”的目标体验一致。"
    )

    async def main():
         await flows_filler.fill(
            FlowsFillerInput(user_requirements, test_actors, test_features, test_business_objects, test_flows, test_perception_slot)
        )
    asyncio.run(main())

    flows_filler_result = """
{
  "business_objects": [
    {
      "business_object_id": 9,
      "business_object_name": "播放器运行环境",
      "business_object_description": "播放器在启动过程中的运行环境与系统状态数据，用于记录启动方式、主程序初始化状态以及各功能模块是否已完成加载。",
      "business_object_attributes": [
        {
          "business_object_attribute_name": "runtime_env_id",
          "business_object_attribute_description": "运行环境唯一标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "R-001"
        },
        {
          "business_object_attribute_name": "startup_type",
          "business_object_attribute_description": "播放器启动方式，如用户手动启动或系统快捷方式触发",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "manual"
        },
        {
          "business_object_attribute_name": "core_initialized",
          "business_object_attribute_description": "核心播放内核是否已初始化完成",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": "true"
        },
        {
          "business_object_attribute_name": "library_module_initialized",
          "business_object_attribute_description": "音乐库模块是否已完成初始化",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": "true"
        },
        {
          "business_object_attribute_name": "ui_module_initialized",
          "business_object_attribute_description": "界面模块是否已完成初始化",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": "true"
        },
        {
          "business_object_attribute_name": "effect_module_initialized",
          "business_object_attribute_description": "音效与均衡器模块是否已完成初始化",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": "true"
        },
        {
          "business_object_attribute_name": "shortcut_module_initialized",
          "business_object_attribute_description": "全局快捷键模块是否已完成初始化",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": "true"
        },
        {
          "business_object_attribute_name": "lyric_module_initialized",
          "business_object_attribute_description": "歌词关联与显示模块是否已完成初始化",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": "true"
        }
      ]
    },
    {
      "business_object_id": 10,
      "business_object_name": "播放器全局配置",
      "business_object_description": "播放器持久化保存的全局配置数据，用于记录音乐库索引路径、会话恢复开关、界面、音效、快捷键等配置的引用信息。",
      "business_object_attributes": [
        {
          "business_object_attribute_name": "global_config_id",
          "business_object_attribute_description": "全局配置唯一标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "GC-001"
        },
        {
          "business_object_attribute_name": "music_library_paths",
          "business_object_attribute_description": "音乐库扫描或索引的本地目录路径列表",
          "business_object_attribute_type": "array[string]",
          "business_object_attribute_example": "[\"D:\\\\Music\", \"E:\\\\Lossless\"]"
        },
        {
          "business_object_attribute_name": "session_restore_enabled",
          "business_object_attribute_description": "是否启用启动时自动恢复上次播放会话",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": "true"
        },
        {
          "business_object_attribute_name": "last_playback_session_id",
          "business_object_attribute_description": "上次退出时保存的播放会话标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "PS-001"
        },
        {
          "business_object_attribute_name": "last_playlist_id",
          "business_object_attribute_description": "上次播放使用的歌单或列表标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "PL-001"
        },
        {
          "business_object_attribute_name": "current_ui_preference_id",
          "business_object_attribute_description": "当前启用的界面偏好设置标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "UI-001"
        },
        {
          "business_object_attribute_name": "current_effect_config_id",
          "business_object_attribute_description": "当前启用的音效配置标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "EQ-001"
        },
        {
          "business_object_attribute_name": "current_shortcut_config_id",
          "business_object_attribute_description": "当前启用的快捷键配置标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "SC-001"
        }
      ]
    },
    {
      "business_object_id": 11,
      "business_object_name": "音乐库索引状态",
      "business_object_description": "播放器当前本地音乐库索引的状态数据，用于记录索引是否初始化、有效歌曲数量及无效条目统计。",
      "business_object_attributes": [
        {
          "business_object_attribute_name": "library_index_id",
          "business_object_attribute_description": "音乐库索引状态唯一标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "LIB-001"
        },
        {
          "business_object_attribute_name": "is_initialized",
          "business_object_attribute_description": "音乐库索引是否已经初始化",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": "true"
        },
        {
          "business_object_attribute_name": "total_music_count",
          "business_object_attribute_description": "索引中的歌曲总数量",
          "business_object_attribute_type": "integer",
          "business_object_attribute_example": "1200"
        },
        {
          "business_object_attribute_name": "invalid_entry_count",
          "business_object_attribute_description": "索引中指向不存在或不可用文件的条目数量",
          "business_object_attribute_type": "integer",
          "business_object_attribute_example": "5"
        }
      ]
    },
    {
      "business_object_id": 12,
      "business_object_name": "快捷键冲突记录",
      "business_object_description": "全局快捷键注册时产生的冲突信息记录，用于提示用户哪些快捷键被系统或其他应用占用。",
      "business_object_attributes": [
        {
          "business_object_attribute_name": "conflict_record_id",
          "business_object_attribute_description": "快捷键冲突记录唯一标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "KC-001"
        },
        {
          "business_object_attribute_name": "shortcut_config_id",
          "business_object_attribute_description": "发生冲突的快捷键配置标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "SC-001"
        },
        {
          "business_object_attribute_name": "conflict_keys",
          "business_object_attribute_description": "存在冲突的快捷键组合列表",
          "business_object_attribute_type": "array[string]",
          "business_object_attribute_example": "[\"Ctrl+Alt+Space\"]"
        },
        {
          "business_object_attribute_name": "conflict_message",
          "business_object_attribute_description": "快捷键冲突提示信息",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "Ctrl+Alt+Space 已被系统占用，已自动禁用该快捷键。"
        }
      ]
    },
    {
      "business_object_id": 13,
      "business_object_name": "会话恢复决策",
      "business_object_description": "用于在启动时决策是否恢复上次播放会话的中间状态数据，记录会话恢复开关、资源可用性以及最终决策结果。",
      "business_object_attributes": [
        {
          "business_object_attribute_name": "restore_decision_id",
          "business_object_attribute_description": "会话恢复决策唯一标识",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "RD-001"
        },
        {
          "business_object_attribute_name": "session_restore_enabled",
          "business_object_attribute_description": "配置是否要求启用会话恢复",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": "true"
        },
        {
          "business_object_attribute_name": "last_session_exists",
          "business_object_attribute_description": "是否存在上次保存的播放会话数据",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": "true"
        },
        {
          "business_object_attribute_name": "last_music_available",
          "business_object_attribute_description": "上次播放的歌曲是否仍可用",
          "business_object_attribute_type": "bool",
          "business_object_attribute_example": "true"
        },
        {
          "business_object_attribute_name": "decision_result",
          "business_object_attribute_description": "最终决策结果，取值如 restore 或 idle",
          "business_object_attribute_type": "string",
          "business_object_attribute_example": "restore"
        }
      ]
    }
  ],
  "flows": [
    {
      "flow_name": "播放器启动与会话恢复流程",
      "flow_description": "用户启动播放器后，系统加载本地音乐库索引、界面与音效偏好、全局快捷键绑定和歌词关联配置，并根据用户设置决定是否恢复上次播放会话，使播放器在启动时即处于就绪状态。",
      "feature_ids": [
        3,
        4,
        5,
        11,
        12,
        13,
        15,
        16,
        17,
        19,
        20,
        21,
        23,
        24,
        25,
        27,
        28,
        29
      ],
      "flow_steps": [
        {
          "step_number": "S-001",
          "step_name": "触发播放器启动",
          "step_description": "用户通过桌面图标、开始菜单或系统快捷方式启动播放器应用，系统初始化基础运行环境。",
          "actor_ids": [
            1,
            2,
            3,
            4,
            5,
            6,
            7
          ],
          "step_type": "actorAction",
          "input_business_object_ids": [
            10
          ],
          "output_business_object_ids": [
            9
          ],
          "next_steps": [
            "S-002"
          ]
        },
        {
          "step_number": "S-002",
          "step_name": "加载基础配置与偏好数据",
          "step_description": "系统读取上次保存的全局配置，包括音乐库索引路径信息、界面显示样式与布局偏好、音效与均衡器参数、歌词同步偏移与关联信息、全局快捷键配置以及上次播放会话状态记录。",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_ids": [
            9,
            10,
            8,
            5,
            4,
            7,
            2,
            3
          ],
          "output_business_object_ids": [
            10,
            8,
            5,
            4,
            7,
            2,
            3
          ],
          "next_steps": [
            "S-003"
          ]
        },
        {
          "step_number": "S-003",
          "step_name": "加载本地音乐库索引",
          "step_description": "系统根据已保存的音乐库索引信息加载本地歌曲列表；若索引缺失或为空，则标记为未初始化状态，准备在界面中提示用户扫描或导入本地音乐。",
          "actor_ids": [],
          "step_type": "systemAction",
          "input_business_object_ids": [
            10,
            1,
            11
          ],
          "output_business_object_ids": [
            1,
            11
          ],
          "next_steps": [
            "S-004"
          ]
        },
        {
          "step_number": "S-004",
          "step_name": "应用界面显示样式与布局",
          "step_description": "系统根据用户界面偏好设置应用主题视觉风格、是否启用轻量化布局、显示/隐藏附加视觉元素，并构建主界面基础结构。",
          "actor_ids": [
            7
          ],
          "step_type": "systemAction",
          "input_business_object_ids": [
            8,
            9
          ],
          "output_business_object_ids": [
            8,
            9
          ],
          "next_steps": [
            "S-005"
          ]
        },
        {
          "step_number": "S-005",
          "step_name": "应用音效与均衡器配置",
          "step_description": "系统加载并应用用户上次保存的音效预设、均衡器各频段参数以及其他音效相关配置，作为当前播放会话的默认输出效果。",
          "actor_ids": [
            3
          ],
          "step_type": "systemAction",
          "input_business_object_ids": [
            5,
            9
          ],
          "output_business_object_ids": [
            5,
            9
          ],
          "next_steps": [
            "S-006"
          ]
        },
        {
          "step_number": "S-006",
          "step_name": "注册全局快捷键",
          "step_description": "系统根据已保存的快捷键绑定配置注册全局播放控制快捷键，并校验是否存在与系统或其他应用的冲突；遇到冲突时仅禁用有问题的绑定并记录提示信息。",
          "actor_ids": [
            6
          ],
          "step_type": "systemAction",
          "input_business_object_ids": [
            7,
            9
          ],
          "output_business_object_ids": [
            7,
            9,
            12
          ],
          "next_steps": [
            "S-007"
          ]
        },
        {
          "step_number": "S-007",
          "step_name": "恢复歌词关联与同步偏移",
          "step_description": "系统加载本地歌曲与歌词文件的关联关系以及每首歌对应的时间偏移设置，为后续播放时的歌词显示做好准备。",
          "actor_ids": [
            4
          ],
          "step_type": "systemAction",
          "input_business_object_ids": [
            4,
            1,
            9
          ],
          "output_business_object_ids": [
            4,
            9
          ],
          "next_steps": [
            "S-008"
          ]
        },
        {
          "step_number": "S-008",
          "step_name": "判断是否启用会话恢复",
          "step_description": "系统根据用户偏好判断是否在启动时自动恢复上次播放会话，包括上次播放的歌曲、播放位置和播放/暂停状态。",
          "actor_ids": [],
          "step_type": "judgment",
          "input_business_object_ids": [
            10,
            2,
            1,
            13
          ],
          "output_business_object_ids": [
            13
          ],
          "next_steps": [
            "S-009",
            "S-010"
          ]
        },
        {
          "step_number": "S-009",
          "step_name": "恢复上次播放会话",
          "step_description": "在用户启用会话恢复的前提下，系统检查上次播放歌曲是否仍存在于本地音乐库：若存在则定位到该歌曲、恢复对应歌单或列表位置，并将播放进度和播放/暂停状态恢复到上次退出时的状态（通常以暂停或待播放状态呈现，避免突兀出声）。",
          "actor_ids": [
            1,
            2
          ],
          "step_type": "systemAction",
          "input_business_object_ids": [
            2,
            3,
            1,
            4,
            13
          ],
          "output_business_object_ids": [
            2,
            3
          ],
          "next_steps": [
            "S-011"
          ]
        },
        {
          "step_number": "S-010",
          "step_name": "进入默认空闲就绪状态",
          "step_description": "当用户未启用会话恢复或上次播放资源已无法使用时，系统保持播放器处于空闲状态，仅展示默认首页界面、最近播放或默认歌单入口，等待用户手动选择歌曲开始播放。",
          "actor_ids": [
            1,
            2
          ],
          "step_type": "systemAction",
          "input_business_object_ids": [
            11,
            3,
            8
          ],
          "output_business_object_ids": [
            2
          ],
          "next_steps": [
            "S-011"
          ]
        },
        {
          "step_number": "S-011",
          "step_name": "提示扫描或导入本地音乐（可选）",
          "step_description": "若系统判定当前音乐库为空或仅包含少量无效条目，则在主界面以简洁方式提示用户执行本地目录扫描或手动导入音乐文件，但不强制弹出打断操作，以保持界面简洁纯净。",
          "actor_ids": [
            1,
            2
          ],
          "step_type": "systemAction",
          "input_business_object_ids": [
            11,
            8
          ],
          "output_business_object_ids": [
            11
          ],
          "next_steps": [
            "S-012"
          ]
        },
        {
          "step_number": "S-012",
          "step_name": "完成启动并进入正常使用",
          "step_description": "系统完成全部初始化与恢复逻辑，将控制权交给用户，用户此时可以直接进行播放控制、管理歌单、调整音效、查看歌词或通过全局快捷键控制播放器。",
          "actor_ids": [
            1,
            2,
            3,
            4,
            5,
            6,
            7
          ],
          "step_type": "systemAction",
          "input_business_object_ids": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13
          ],
          "output_business_object_ids": [
            9
          ],
          "next_steps": []
        }
      ]
    }
  ]
}
"""
