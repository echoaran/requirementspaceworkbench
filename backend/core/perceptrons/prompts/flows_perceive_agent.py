flows_perceive_prompt = """
# 角色
你是一个善于设计项目流程的软件设计师。

# 任务
1. 分析用户用自然语言描述的项目需求、目标系统参与者（用户）、目标系统能力（features）与当前整理出的系统流程（包括输入输出的结构）。
2. 判断是否需要补充系统流程（注意不是流程步骤，是流程）。若需要，则描述需要补充什么，为何需要补充，如何补充；若不需要，则输出不需要。
3. 按照下方规定输出格式输出补充系统流程的原因。

# 用户需求
{{user_requirements}}

# 参与者（用户）
{{actors}}

# 系统能力（features）
{{features}}

# 当前整理出的流程
{{flows}}

# 输出格式说明
{
    "perceptionDescription": "<‘描述需要补充什么，为何需要补充，如何补充’ | 不需要>"
}

# 规则
1. 只输出一个 JSON 对象。
2. 不要输出任何解释、分析过程、Markdown、代码块标记或额外前后缀文字。
3. 输出 JSON 风格的标准格式化内容，而不是被压缩的一行内容。

# 示例
## 示例输入
### 用户需求
轻量化桌面悬浮便签 + 待办整合软件，可新建多个独立便签贴在桌面任意位置，支持文字编辑、颜色分类、字体调整；自带待办清单功能，可设置任务截止时间、已完成标记、置顶重要事项，支持开机常驻、透明化背景、一键隐藏所有便签，适合学生、上班族记录临时灵感、日程、琐事。
### 参与者（用户）
{
    "actors": [
        {
            "actor_id": 1,
            "actor_name": "普通用户",
            "actor_description": "使用本软件进行便签记录、待办任务管理的学生、上班族等个人使用者"
        }
    ]
}
### 系统能力（features）
{
    "features": [
        {
            "feature_id": 1, 
            "feature_name": "便签创建与布局",
            "feature_description": "支持新建多个独立便签，并可将便签拖动放置在桌面任意位置",
            "actor_ids": [1]
        },
        {
            "feature_id": 2, 
            "feature_name": "便签文字编辑",
            "feature_description": "提供便签内文字的输入、修改、删除等基础编辑功能",
            "actor_ids": [1]
        },
        {
            "feature_id": 3, 
            "feature_name": "便签样式设置",
            "feature_description": "支持便签颜色分类和字体样式、大小的调整",
            "actor_ids": [1],
        },
        {
            "feature_id": 4, 
            "feature_name": "任务创建与截止时间设置",
            "feature_description": "支持创建待办任务，并为任务设置截止时间",
            "actor_ids": [1],
        },
        {
            "feature_id": 5, 
            "feature_name": "任务完成状态标记",
            "feature_description": "支持将已完成的待办任务进行标记区分",
            "actor_ids": [1],
        },
        {
            "feature_id": 6, 
            "feature_name": "重要任务置顶",
            "feature_description": "支持将重要的待办任务置顶显示，突出优先级",
            "actor_ids": [1],
        },
        {
            "feature_id": 7, 
            "feature_name": "开机常驻设置",
            "feature_description": "支持设置软件随系统开机自动启动并常驻后台运行",
            "actor_ids": [1],
        },
        {
            "feature_id": 8, 
            "feature_name": "便签背景透明化",
            "feature_description": "支持调整便签背景的透明度，减少对桌面内容的遮挡",
            "actor_ids": [1],
        },
        {
            "feature_id": 9, 
            "feature_name": "一键隐藏所有便签",
            "feature_description": "提供一键操作，快速隐藏桌面上所有的悬浮便签",
            "actor_ids": [1],
        }
    ]
}
### 当前整理出的流程（包括输入输出的结构）
{
    "business_objects": [
        {
            "business_object_id": 1,
            "business_object_name": "便签",
            "business_object_description": "用户创建的悬浮在桌面的独立便签实体，包含内容、样式和位置信息",
            "business_object_attributes": [
                {
                    "business_object_attribute_name": "note_id",
                    "business_object_attribute_description": "便签唯一标识符",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "note_20260517_001"
                },
                {
                    "business_object_attribute_name": "content",
                    "business_object_attribute_description": "便签内的文字内容",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "下午3点参加项目周会"
                },
                {
                    "business_object_attribute_name": "position",
                    "business_object_attribute_description": "便签在桌面的坐标位置",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "200,150"
                },
                {
                    "business_object_attribute_name": "color",
                    "business_object_attribute_description": "便签背景颜色",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "#FFE4B5"
                },
                {
                    "business_object_attribute_name": "font_family",
                    "business_object_attribute_description": "便签文字字体",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "微软雅黑"
                },
                {
                    "business_object_attribute_name": "font_size",
                    "business_object_attribute_description": "便签文字字号",
                    "business_object_attribute_type": "integer",
                    "business_object_attribute_example": "14"
                },
                {
                    "business_object_attribute_name": "transparency",
                    "business_object_attribute_description": "便签背景透明度（0-100）",
                    "business_object_attribute_type": "integer",
                    "business_object_attribute_example": "80"
                },
                {
                    "business_object_attribute_name": "is_hidden",
                    "business_object_attribute_description": "便签是否处于隐藏状态",
                    "business_object_attribute_type": "bool",
                    "business_object_attribute_example": "false"
                },
                {
                    "business_object_attribute_name": "create_time",
                    "business_object_attribute_description": "便签创建时间",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "2026-05-17 10:30:00"
                },
                {
                    "business_object_attribute_name": "update_time",
                    "business_object_attribute_description": "便签最后更新时间",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "2026-05-17 10:35:00"
                }
            ]
        },
        {
            "business_object_id": 2,
            "business_object_name": "待办任务",
            "business_object_description": "用户创建的待办事项实体，包含任务内容、截止时间和状态信息",
            "business_object_attributes": [
                {
                    "business_object_attribute_name": "task_id",
                    "business_object_attribute_description": "待办任务唯一标识符",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "task_20260517_001"
                },
                {
                    "business_object_attribute_name": "content",
                    "business_object_attribute_description": "待办任务内容",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "完成需求文档撰写"
                },
                {
                    "business_object_attribute_name": "deadline",
                    "business_object_attribute_description": "任务截止时间",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "2026-05-20 18:00:00"
                },
                {
                    "business_object_attribute_name": "is_completed",
                    "business_object_attribute_description": "任务是否已完成",
                    "business_object_attribute_type": "bool",
                    "business_object_attribute_example": "false"
                },
                {
                    "business_object_attribute_name": "is_pinned",
                    "business_object_attribute_description": "任务是否置顶显示",
                    "business_object_attribute_type": "bool",
                    "business_object_attribute_example": "true"
                },
                {
                    "business_object_attribute_name": "create_time",
                    "business_object_attribute_description": "任务创建时间",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "2026-05-17 11:00:00"
                },
                {
                    "business_object_attribute_name": "update_time",
                    "business_object_attribute_description": "任务最后更新时间",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "2026-05-17 11:05:00"
                }
            ]
        },
        {
            "business_object_id": 3,
            "business_object_name": "系统全局设置",
            "business_object_description": "软件的全局配置信息，包含开机启动、显示控制等设置",
            "business_object_attributes": [
                {
                    "business_object_attribute_name": "auto_start",
                    "business_object_attribute_description": "是否随系统开机自动启动",
                    "business_object_attribute_type": "bool",
                    "business_object_attribute_example": "true"
                },
                {
                    "business_object_attribute_name": "all_notes_hidden",
                    "business_object_attribute_description": "所有便签是否处于全局隐藏状态",
                    "business_object_attribute_type": "bool",
                    "business_object_attribute_example": "false"
                },
                {
                    "business_object_attribute_name": "default_note_color",
                    "business_object_attribute_description": "新建便签默认背景颜色",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "#FFFFE0"
                },
                {
                    "business_object_attribute_name": "default_font_size",
                    "business_object_attribute_description": "新建便签默认文字字号",
                    "business_object_attribute_type": "integer",
                    "business_object_attribute_example": "14"
                }
            ]
        }
    ],
    "flows": [
        {
            "flow_name": "便签创建与管理流程",
            "flow_description": "用户创建、编辑、调整样式和位置、设置透明度并管理便签的完整流程",
            "feature_ids": [1, 2, 3, 8],
            "flow_steps": [
                {
                    "step_id": 1,
                    "step_name": "触发新建便签",
                    "step_description": "用户通过右键菜单或快捷键触发新建便签操作",
                    "actor_ids": [1],
                    "step_type": "actorAction",
                    "input_business_object_ids": [],
                    "output_business_object_ids": [1],
                    "next_step_ids": [2]
                },
                {
                    "step_id": 2,
                    "step_name": "创建并显示空白便签",
                    "step_description": "系统根据默认设置创建空白便签并显示在桌面默认位置",
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": [1, 3],
                    "output_business_object_ids": [1],
                    "next_step_ids": [3, 4, 5, 6, 7]
                },
                {
                    "step_id": 3,
                    "step_name": "编辑便签内容",
                    "step_description": "用户在便签内输入、修改或删除文字内容",
                    "actor_ids": [1],
                    "step_type": "actorAction",
                    "input_business_object_ids": [1],
                    "output_business_object_ids": [1],
                    "next_step_ids": [4, 5, 6, 7]
                },
                {
                    "step_id": 4,
                    "step_name": "调整便签位置",
                    "step_description": "用户拖动便签到桌面任意位置",
                    "actor_ids": [1],
                    "step_type": "actorAction",
                    "input_business_object_ids": [1],
                    "output_business_object_ids": [1],
                    "next_step_ids": [3, 5, 6, 7]
                },
                {
                    "step_id": 5,
                    "step_name": "设置便签样式",
                    "step_description": "用户选择便签背景颜色、调整字体样式和字号",
                    "actor_ids": [1],
                    "step_type": "actorAction",
                    "input_business_object_ids": [1],
                    "output_business_object_ids": [1],
                    "next_step_ids": [3, 4, 6, 7]
                },
                {
                    "step_id": 6,
                    "step_name": "调整便签透明度",
                    "step_description": "用户拖动滑块调整便签背景的透明度",
                    "actor_ids": [1],
                    "step_type": "actorAction",
                    "input_business_object_ids": [1],
                    "output_business_object_ids": [1],
                    "next_step_ids": [3, 4, 5, 7]
                },
                {
                    "step_id": 7,
                    "step_name": "保存便签修改",
                    "step_description": "系统自动保存便签的所有修改内容",
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": [1],
                    "output_business_object_ids": [1],
                    "next_step_ids": []
                }
            ]
        },
        {
            "flow_name": "待办任务管理流程",
            "flow_description": "用户创建待办任务、设置截止时间、标记完成状态和置顶重要任务的流程",
            "feature_ids": [4, 5, 6],
            "flow_steps": [
                {
                    "step_id": 1,
                    "step_name": "触发新建待办任务",
                    "step_description": "用户在待办清单界面点击新建按钮触发任务创建",
                    "actor_ids": [1],
                    "step_type": "actorAction",
                    "input_business_object_ids": [],
                    "output_business_object_ids": [2],
                    "next_step_ids": [2]
                },
                {
                    "step_id": 2,
                    "step_name": "创建并显示空白任务",
                    "step_description": "系统创建空白待办任务并显示在待办清单中",
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": [2],
                    "output_business_object_ids": [2],
                    "next_step_ids": [3, 4, 5, 6, 7]
                },
                {
                    "step_id": 3,
                    "step_name": "输入任务内容",
                    "step_description": "用户输入待办任务的具体内容",
                    "actor_ids": [1],
                    "step_type": "actorAction",
                    "input_business_object_ids": [2],
                    "output_business_object_ids": [2],
                    "next_step_ids": [4, 5, 6, 7]
                },
                {
                    "step_id": 4,
                    "step_name": "设置任务截止时间",
                    "step_description": "用户选择并设置任务的截止日期和时间",
                    "actor_ids": [1],
                    "step_type": "actorAction",
                    "input_business_object_ids": [2],
                    "output_business_object_ids": [2],
                    "next_step_ids": [3, 5, 6, 7]
                },
                {
                    "step_id": 5,
                    "step_name": "标记任务完成状态",
                    "step_description": "用户点击复选框标记任务为已完成或未完成",
                    "actor_ids": [1],
                    "step_type": "actorAction",
                    "input_business_object_ids": [2],
                    "output_business_object_ids": [2],
                    "next_step_ids": [3, 4, 6, 7]
                },
                {
                    "step_id": 6,
                    "step_name": "置顶重要任务",
                    "step_description": "用户点击置顶按钮将重要任务显示在清单顶部",
                    "actor_ids": [1],
                    "step_type": "actorAction",
                    "input_business_object_ids": [2],
                    "output_business_object_ids": [2],
                    "next_step_ids": [3, 4, 5, 7]
                },
                {
                    "step_id": 7,
                    "step_name": "保存任务修改",
                    "step_description": "系统自动保存待办任务的所有修改内容",
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": [2],
                    "output_business_object_ids": [2],
                    "next_step_ids": []
                }
            ]
        },
        {
            "flow_name": "系统全局设置流程",
            "flow_description": "用户设置软件开机常驻、一键隐藏所有便签等全局功能的流程",
            "feature_ids": [7, 9],
            "flow_steps": [
                {
                    "step_id": 1,
                    "step_name": "打开系统设置界面",
                    "step_description": "用户通过托盘图标右键菜单打开系统设置界面",
                    "actor_ids": [1],
                    "step_type": "actorAction",
                    "input_business_object_ids": [],
                    "output_business_object_ids": [3],
                    "next_step_ids": [2]
                },
                {
                    "step_id": 2,
                    "step_name": "加载当前系统设置",
                    "step_description": "系统加载并显示当前的全局配置信息",
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": [3],
                    "output_business_object_ids": [3],
                    "next_step_ids": [3, 4, 5]
                },
                {
                    "step_id": 3,
                    "step_name": "设置开机常驻选项",
                    "step_description": "用户勾选或取消开机自动启动选项",
                    "actor_ids": [1],
                    "step_type": "actorAction",
                    "input_business_object_ids": [3],
                    "output_business_object_ids": [3],
                    "next_step_ids": [4, 5]
                },
                {
                    "step_id": 4,
                    "step_name": "一键隐藏所有便签",
                    "step_description": "用户点击一键隐藏按钮或使用快捷键隐藏所有桌面便签",
                    "actor_ids": [1],
                    "step_type": "actorAction",
                    "input_business_object_ids": [3, 1],
                    "output_business_object_ids": [3, 1],
                    "next_step_ids": [3, 5]
                },
                {
                    "step_id": 5,
                    "step_name": "保存系统设置",
                    "step_description": "系统保存用户修改后的全局配置信息",
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": [3],
                    "output_business_object_ids": [3],
                    "next_step_ids": []
                }
            ]
        }
    ]
}

## 示例输出
{
    "perceptionDescription": "不需要"
}
"""