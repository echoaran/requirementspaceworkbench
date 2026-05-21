from dataclasses import dataclass
import json
from typing import Dict, List

from backend.core.perceptrons.prompts import features_perceive_prompt
from backend.core.perceptrons.base_perceptron import BasePerceptron, PerceptronInput
from backend.schemas import ActorNode, FeatureNode


# 为系统功能感知器定义专属的输入类型
@dataclass
class FeaturesPerceptronInput(PerceptronInput):
    user_requirements: str
    actors: List[ActorNode]
    features: List[FeatureNode]

class FeaturesPerceptron(BasePerceptron[FeaturesPerceptronInput]):
    async def perceive(self, input_data: FeaturesPerceptronInput) -> Dict:
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
            prompt=features_perceive_prompt.replace(
                "{{user_requirements}}",f"{user_requirements_}").replace(
                "{{actors}}", f"{actors_}").replace(
                "{{features}}", f"{features_}"
            ),
            print_log=False,
        )
        return json.loads(response)

if __name__ == "__main__":
    import asyncio
    features_perceptron = FeaturesPerceptron()

    user_requirements = "极简纯净本地音乐播放器，不联网、无会员、无广告，只读取电脑本地音乐文件，支持无损格式 Flac/WAV/MP3 播放，自带歌词本地匹配、音效均衡器、歌单自定义、睡眠定时关闭、全局快捷键切歌，界面清爽轻量化，替代臃肿的主流音乐播放器。"
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
    async def main():
        features_perceptron_result = await features_perceptron.perceive(
            FeaturesPerceptronInput(user_requirements, test_actors, test_features)
        )
    asyncio.run(main())

    result = """
{
  "perceptionDescription": "需要补充。用户需求描述中强调播放器需“保持清爽、轻量、低干扰的使用体验”，且是一个本地音乐播放器，但当前功能集中在播放控制、音效、歌词、歌单、定时和界面外观，没有体现一些核心的基础能力和关键的体验相关能力：\n\n1）缺少基础播放模式与队列管理功能。\n- 为何需要：本地音乐听众通常需要循环播放、单曲循环、随机播放、顺序播放等模式，以及当前播放队列的查看与管理，否则难以控制长时间听歌时的播放行为。歌单管理者在整理歌单后，也需要将歌单内容加入播放队列并按队列顺序播放。\n- 如何补充：\n  - 新增“播放模式与队列管理”功能，包含：\n    - 播放模式切换（顺序播放、列表循环、单曲循环、随机播放）。\n    - 当前播放队列查看（显示当前将依次播放的歌曲列表）。\n    - 队列编辑（从队列中移除歌曲、临时添加歌曲、拖拽调整队列顺序）。\n  - 关联参与者：本地音乐听众（1）、歌单管理者（2）。\n\n2）缺少基础媒体信息展示与歌曲信息管理。\n- 为何需要：本地音乐听众在播放时通常需要查看当前歌曲的标题、歌手、专辑、时长、封面等，便于识别正在播放的内容；歌单管理者在整理歌单时需要依赖歌曲的基础信息进行分类和筛选。缺少这些会影响基本可用性和整理体验。\n- 如何补充：\n  - 新增“歌曲信息展示与管理”功能，包含：\n    - 播放界面展示当前歌曲的基础信息（标题、歌手、专辑、时长、封面）。\n    - 歌曲列表中展示基础信息字段，并支持按常用字段排序（如标题、歌手、专辑、添加时间）。\n    - 简单的本地标签编辑（例如修改歌曲显示名、为歌曲添加简单标签或备注，不必做完整 ID3 标签编辑器，但要满足整理需求）。\n  - 关联参与者：本地音乐听众（1）、歌单管理者（2）。\n\n3）缺少基础搜索与筛选功能。\n- 为何需要：本地音乐库一旦规模较大，如果只能通过列表和歌单浏览来选歌，效率很低；用户需求中虽然未直接提“搜索”，但这是本地播放器的隐含刚需，否则“导入/扫描本地音乐”后难以快速定位歌曲，特别是对歌单管理者建立歌单时的选曲体验影响较大。\n- 如何补充：\n  - 新增“本地音乐搜索与筛选”功能，包含：\n    - 按歌曲名、歌手、专辑关键字搜索本地音乐。\n    - 按基础属性筛选（例如按文件夹来源、音频格式、最近添加/最近播放等）以便快速定位目标歌曲。\n  - 关联参与者：本地音乐听众（1）、歌单管理者（2）。\n\n4）缺少基础播放历史与最近播放记录。\n- 为何需要：许多用户会临时听到喜欢的歌曲，之后希望回溯“刚刚播放过的歌曲”；歌单管理者也可能希望根据历史播放情况整理“常听歌单”。没有播放历史，会影响体验和轻量化使用的连续性。\n- 如何补充：\n  - 新增“播放历史与最近播放”功能，包含：\n    - 自动记录最近播放的歌曲列表。\n    - 支持从“最近播放”中快速重新播放或加入当前播放队列/歌单。\n  - 关联参与者：本地音乐听众（1）、歌单管理者（2）。\n\n5）缺少最小化到系统托盘与低干扰状态控制。\n- 为何需要：需求强调“轻量、低干扰”，但当前界面相关功能仅涉及样式、布局和视觉风格，没有涉及最关键的“存在方式”：例如最小化到系统托盘、在任务栏中低存在感显示、快速呼出/隐藏。对长期后台播放音乐的用户，这类能力是低干扰体验的关键。\n- 如何补充：\n  - 新增“低干扰运行与托盘控制”功能，包含：\n    - 支持最小化到系统托盘，关闭窗口但保持后台播放。\n    - 托盘图标菜单支持基础播放控制（播放/暂停、上一首、下一首、退出）。\n    - 可配置是否在任务栏显示主窗口或仅驻留托盘。\n  - 关联参与者：界面偏好设置者（7）、本地音乐听众（1）、快捷键控制者（6）。\n\n6）缺少基础音量控制与静音。\n- 为何需要：播放控制 feature 中目前未体现音量调节与静音，而这是本地播放器的基础操作之一。虽然可以偏向“清爽、轻量”，但音量控制是刚需，否则用户只能通过系统整体音量调节，体验不佳。\n- 如何补充：\n  - 扩展“播放控制”功能描述，增加：\n    - 播放音量增减、静音/取消静音。\n    - 可选地支持每首歌保持统一音量（简单的音量标准化选项，可以作为后续扩展）。\n  - 关联参与者：本地音乐听众（1）、快捷键控制者（6）（如果支持音量快捷键，可后续新增子能力）。\n\n7）缺少基础应用设置与配置管理（除界面外观外）。\n- 为何需要：当前只有界面视觉偏好、睡眠定时、快捷键、音效等各自的局部设置，但缺少一个统一的“应用设置/偏好”能力，用于管理扫描目录、默认播放行为、默认歌词匹配策略等基础配置；这会直接影响“长期使用”的轻量与可控性。\n- 如何补充：\n  - 新增“应用通用设置与配置管理”功能，包含：\n    - 默认音乐库目录管理（设置/修改扫描目录，开机后是否自动扫描更新）。\n    - 默认播放行为设置（例如双击时是插入当前队列后播放还是替换队列等）。\n    - 默认歌词匹配策略（优先本地文件夹、是否自动尝试网络匹配——若项目明确只离线则可仅保留本地策略开关）。\n    - 全局语言/基础行为（例如是否开机自启，如果产品范围允许）。\n  - 关联参与者：本地音乐听众（1）、界面偏好设置者（7）。\n\n这些补充功能主要围绕“本地音乐播放器”作为产品类型的隐含基础需求，以及“轻量、低干扰、长期使用”目标下的运行与交互方式，能让现有的播放、歌单、歌词、音效、定时、快捷键和界面功能在真实使用场景中形成一个完整、可用且体验一致的系统。"
}
"""