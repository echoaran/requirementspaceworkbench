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
            "actor_name": "便签记录者",
            "actor_description": "便签记录者是指在需要快速记录临时灵感、课程内容、会议要点、日程安排或生活琐事的场景下，与桌面便签功能发生交互，并可执行新建便签、编辑文字内容、查看便签和删除便签等操作的用户角色。"
        },
        {
            "actor_id": 2,
            "actor_name": "便签整理者",
            "actor_description": "便签整理者是指在需要对桌面上的多条便签进行分类、区分和排布的场景下，与便签管理功能发生交互，并可执行移动便签位置、设置颜色分类、调整字体样式、调整便签外观和管理多个独立便签等操作的用户角色。"
        },
        {
            "actor_id": 3,
            "actor_name": "待办管理者",
            "actor_description": "待办管理者是指在需要规划、跟踪和处理个人任务的场景下，与待办清单功能发生交互，并可执行创建待办事项、设置任务截止时间、标记任务已完成、查看任务状态和置顶重要事项等操作的用户角色。"
        },
        {
             "actor_id": 4,
            "actor_name": "桌面显示控制者",
            "actor_description": "桌面显示控制者是指在需要控制便签在桌面上的显示状态、降低桌面干扰或保持重要信息可见的场景下，与桌面悬浮显示功能发生交互，并可执行设置透明化背景、一键隐藏所有便签、恢复显示便签和控制便签常驻桌面等操作的用户角色。"
        },
        {
            "actor_id": 5,
            "actor_name": "系统偏好设置者",
            "actor_description": "系统偏好设置者是指在需要让软件符合个人长期使用习惯的场景下，与软件设置功能发生交互，并可执行设置开机常驻、配置默认便签样式、调整默认字体、设置默认颜色分类和配置显示偏好等操作的用户角色。"
        }
    ]
}
### 系统能力（features）
{
    "features": [
        {
            "feature_id": 3,
            "feature_name": "新建独立便签",
            "feature_description": "支持用户创建多个相互独立的桌面便签，用于记录临时灵感、课程内容、会议要点、日程安排或生活琐事。",
            "actor_ids": [
                1
            ]
        },
        {
            "feature_id": 4,
            "feature_name": "编辑便签文字",
            "feature_description": "支持用户在便签中输入、修改和查看文字内容。",
            "actor_ids": [
                1
            ]
        },
        {
            "feature_id": 5,
            "feature_name": "管理便签位置",
            "feature_description": "支持用户将多个便签放置在桌面任意位置，便于按照个人习惯组织桌面信息。",
            "actor_ids": [
                2
            ]
        },
        {
            "feature_id": 7,
            "feature_name": "颜色分类",
            "feature_description": "支持用户为便签设置不同颜色，用于区分信息类别、优先级或使用场景。",
            "actor_ids": [
                2,
                5
            ]
        },
        {
            "feature_id": 8,
            "feature_name": "字体调整",
            "feature_description": "支持用户调整便签文字的字体样式，使便签内容更符合个人阅读和整理习惯。",
            "actor_ids": [
                2,
                5
            ]
        },
        {
            "feature_id": 10,
            "feature_name": "创建待办事项",
            "feature_description": "支持用户新增待办任务，用于记录需要完成的学习、工作或生活事项。",
            "actor_ids": [
                3
            ]
        },
        {
            "feature_id": 11,
            "feature_name": "设置任务截止时间",
            "feature_description": "支持用户为待办事项设置截止时间，用于安排任务完成节点和日程计划。",
            "actor_ids": [
                3
            ]
        },
        {
            "feature_id": 12,
            "feature_name": "标记任务完成状态",
            "feature_description": "支持用户将待办事项标记为已完成，用于跟踪任务处理进度。",
            "actor_ids": [
                3
            ]
        },
        {
            "feature_id": 13,
            "feature_name": "置顶重要事项",
            "feature_description": "支持用户将重要待办事项置顶显示，便于优先关注和处理关键任务。",
            "actor_ids": [
                3
            ]
        },
        {
            "feature_id": 15,
            "feature_name": "透明化背景",
            "feature_description": "支持用户设置便签背景透明效果，使便签与桌面环境更协调。",
            "actor_ids": [
                4,
                5
            ]
        },
        {
            "feature_id": 16,
            "feature_name": "一键隐藏所有便签",
            "feature_description": "支持用户一次性隐藏所有桌面便签，用于临时清理桌面显示或减少视觉干扰。",
            "actor_ids": [
                4
            ]
        },
        {
            "feature_id": 17,
            "feature_name": "恢复显示便签",
            "feature_description": "支持用户在隐藏便签后恢复显示所有便签，便于继续查看和处理记录内容。",
            "actor_ids": [
                4
            ]
        },
        {
            "feature_id": 18,
            "feature_name": "开机常驻",
            "feature_description": "支持用户设置软件开机后自动运行并保持常驻，便于随时查看和记录信息。",
            "actor_ids": [
                5
            ]
        },
        {
            "feature_id": 19,
            "feature_name": "默认便签样式配置",
            "feature_description": "支持用户配置默认字体、默认颜色和默认显示样式，减少重复设置操作。",
            "actor_ids": [
                5
            ]
        }
    ]
}
### 当前整理出的流程（包括输入输出的结构）
{
    "business_objects": [
        {
            "business_object_id": 1,
            "business_object_name": "桌面便签",
            "business_object_description": "用户创建并悬浮显示在桌面上的独立便签，用于记录文字信息并承载位置、颜色、字体和显示状态等数据。",
            "business_object_attributes": [
                {
                    "business_object_attribute_name": "note_id",
                    "business_object_attribute_description": "便签唯一标识",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "N-001"
                },
                {
                    "business_object_attribute_name": "content",
                    "business_object_attribute_description": "便签文字内容",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "下午三点提交课程作业"
                },
                {
                    "business_object_attribute_name": "position_x",
                    "business_object_attribute_description": "便签在桌面上的横向坐标",
                    "business_object_attribute_type": "integer",
                    "business_object_attribute_example": "320"
                },
                {
                    "business_object_attribute_name": "position_y",
                    "business_object_attribute_description": "便签在桌面上的纵向坐标",
                    "business_object_attribute_type": "integer",
                    "business_object_attribute_example": "180"
                },
                {
                    "business_object_attribute_name": "color_category",
                    "business_object_attribute_description": "便签颜色分类",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "黄色"
                },
                {
                    "business_object_attribute_name": "font_family",
                    "business_object_attribute_description": "便签字体名称",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "Microsoft YaHei"
                },
                {
                    "business_object_attribute_name": "font_size",
                    "business_object_attribute_description": "便签字号",
                    "business_object_attribute_type": "integer",
                    "business_object_attribute_example": "14"
                },
                {
                    "business_object_attribute_name": "opacity",
                    "business_object_attribute_description": "便签背景透明度",
                    "business_object_attribute_type": "decimal",
                    "business_object_attribute_example": "0.75"
                },
                {
                    "business_object_attribute_name": "is_hidden",
                    "business_object_attribute_description": "便签是否处于隐藏状态",
                    "business_object_attribute_type": "bool",
                    "business_object_attribute_example": "false"
                }
            ]
        },
        {
            "business_object_id": 2,
            "business_object_name": "待办事项",
            "business_object_description": "用户创建的个人任务条目，用于记录任务内容、截止时间、完成状态和重要程度。",
            "business_object_attributes": [
                {
                    "business_object_attribute_name": "todo_id",
                    "business_object_attribute_description": "待办事项唯一标识",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "T-001"
                },
                {
                    "business_object_attribute_name": "title",
                    "business_object_attribute_description": "待办事项标题",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "整理会议纪要"
                },
                {
                    "business_object_attribute_name": "due_time",
                    "business_object_attribute_description": "任务截止时间",
                    "business_object_attribute_type": "datetime",
                    "business_object_attribute_example": "2026-05-21 18:00:00"
                },
                {
                    "business_object_attribute_name": "is_completed",
                    "business_object_attribute_description": "任务是否完成",
                    "business_object_attribute_type": "bool",
                    "business_object_attribute_example": "false"
                },
                {
                    "business_object_attribute_name": "is_pinned",
                    "business_object_attribute_description": "任务是否置顶",
                    "business_object_attribute_type": "bool",
                    "business_object_attribute_example": "true"
                }
            ]
        },
        {
            "business_object_id": 3,
            "business_object_name": "显示控制状态",
            "business_object_description": "桌面便签整体显示控制数据，用于记录全局隐藏、恢复显示和常驻桌面等状态。",
            "business_object_attributes": [
                {
                    "business_object_attribute_name": "display_state_id",
                    "business_object_attribute_description": "显示控制状态唯一标识",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "D-001"
                },
                {
                    "business_object_attribute_name": "all_notes_hidden",
                    "business_object_attribute_description": "是否已隐藏所有便签",
                    "business_object_attribute_type": "bool",
                    "business_object_attribute_example": "true"
                },
                {
                    "business_object_attribute_name": "resident_enabled",
                    "business_object_attribute_description": "是否启用桌面常驻",
                    "business_object_attribute_type": "bool",
                    "business_object_attribute_example": "true"
                }
            ]
        },
        {
            "business_object_id": 4,
            "business_object_name": "系统偏好设置",
            "business_object_description": "用户长期使用偏好配置，包括开机常驻、默认颜色、默认字体和默认显示样式。",
            "business_object_attributes": [
                {
                    "business_object_attribute_name": "preference_id",
                    "business_object_attribute_description": "偏好设置唯一标识",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "P-001"
                },
                {
                    "business_object_attribute_name": "auto_start_enabled",
                    "business_object_attribute_description": "是否启用开机自动运行",
                    "business_object_attribute_type": "bool",
                    "business_object_attribute_example": "true"
                },
                {
                    "business_object_attribute_name": "default_color",
                    "business_object_attribute_description": "新建便签默认颜色",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "浅黄色"
                },
                {
                    "business_object_attribute_name": "default_font_family",
                    "business_object_attribute_description": "新建便签默认字体",
                    "business_object_attribute_type": "string",
                    "business_object_attribute_example": "Microsoft YaHei"
                },
                {
                    "business_object_attribute_name": "default_font_size",
                    "business_object_attribute_description": "新建便签默认字号",
                    "business_object_attribute_type": "integer",
                    "business_object_attribute_example": "14"
                },
                {
                    "business_object_attribute_name": "default_opacity",
                    "business_object_attribute_description": "新建便签默认透明度",
                    "business_object_attribute_type": "decimal",
                    "business_object_attribute_example": "0.85"
                }
            ]
        }
    ],
    "flows": [
        {
            "flow_name": "便签创建与编辑流程",
            "flow_description": "便签记录者创建独立桌面便签，并输入、修改和保存便签文字内容。",
            "feature_ids": [
                3,
                4
            ],
            "flow_steps": [
                {
                    "step_id": 1,
                    "step_name": "发起新建便签",
                    "step_description": "便签记录者点击新建便签入口，要求系统创建一个新的独立便签。",
                    "actor_ids": [
                        1
                    ],
                    "step_type": "actorAction",
                    "input_business_object_ids": [],
                    "output_business_object_ids": [],
                    "next_steps": [
                        2
                    ]
                },
                {
                    "step_id": 2,
                    "step_name": "生成空白便签",
                    "step_description": "系统按照默认样式生成空白桌面便签，并分配唯一标识。",
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": [
                        4
                    ],
                    "output_business_object_ids": [
                        1
                    ],
                    "next_steps": [
                        3
                    ]
                },
                {
                    "step_id": 3,
                    "step_name": "输入或修改文字",
                    "step_description": "便签记录者在便签中输入临时灵感、日程、会议要点或生活琐事，也可修改已有内容。",
                    "actor_ids": [
                        1
                    ],
                    "step_type": "actorAction",
                    "input_business_object_ids": [
                        1
                    ],
                    "output_business_object_ids": [
                        1
                    ],
                    "next_steps": [
                        4
                    ]
                },
                {
                    "step_id": 4,
                    "step_name": "保存便签内容",
                    "step_description": "系统保存便签文字内容和更新时间，并保持便签在桌面显示。",
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": [
                        1
                    ],
                    "output_business_object_ids": [
                        1
                    ],
                    "next_steps": []
                }
            ]
        },
        {
            "flow_name": "便签整理与样式调整流程",
            "flow_description": "便签整理者对多个独立便签进行位置管理、颜色分类、字体调整和透明化外观设置。",
            "feature_ids": [
                5,
                7,
                8,
                15
            ],
            "flow_steps": [
                {
                    "step_id": 5,
                    "step_name": "选择目标便签",
                    "step_description": "便签整理者从桌面上的多个便签中选择需要整理或调整样式的便签。",
                    "actor_ids": [
                        2
                    ],
                    "step_type": "actorAction",
                    "input_business_object_ids": [
                        1
                    ],
                    "output_business_object_ids": [
                        1
                    ],
                    "next_steps": [
                        6,
                        7,
                        8,
                        9
                    ]
                },
                {
                    "step_id": 6,
                    "step_name": "拖动便签位置",
                    "step_description": "便签整理者将便签拖动到桌面任意目标位置。",
                    "actor_ids": [
                        2
                    ],
                    "step_type": "actorAction",
                    "input_business_object_ids": [
                        1
                    ],
                    "output_business_object_ids": [
                        1
                    ],
                    "next_steps": [
                        10
                    ]
                },
                {
                    "step_id": 7,
                    "step_name": "设置颜色分类",
                    "step_description": "便签整理者为便签选择颜色，用于区分信息类别、优先级或使用场景。",
                    "actor_ids": [
                        2
                    ],
                    "step_type": "actorAction",
                    "input_business_object_ids": [
                        1
                    ],
                    "output_business_object_ids": [
                        1
                    ],
                    "next_steps": [
                        10
                    ]
                },
                {
                    "step_id": 8,
                    "step_name": "调整字体样式",
                    "step_description": "便签整理者调整便签文字的字体、字号或相关显示样式。",
                    "actor_ids": [
                        2
                    ],
                    "step_type": "actorAction",
                    "input_business_object_ids": [
                        1
                    ],
                    "output_business_object_ids": [
                        1
                    ],
                    "next_steps": [
                        10
                    ]
                },
                {
                    "step_id": 9,
                    "step_name": "设置背景透明度",
                    "step_description": "便签整理者调整便签背景透明效果，使便签与桌面环境协调。",
                    "actor_ids": [
                        4
                    ],
                    "step_type": "actorAction",
                    "input_business_object_ids": [
                        1
                    ],
                    "output_business_object_ids": [
                        1
                    ],
                    "next_steps": [
                        10
                    ]
                },
                {
                    "step_id": 10,
                    "step_name": "保存便签布局与样式",
                    "step_description": "系统保存便签的位置、颜色、字体和透明度设置。",
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": [
                        1
                    ],
                    "output_business_object_ids": [
                        1
                    ],
                    "next_steps": []
                }
            ]
        },
        {
            "flow_name": "待办事项管理流程",
            "flow_description": "待办管理者创建待办事项，设置截止时间，置顶重要事项，并标记任务完成状态。",
            "feature_ids": [
                10,
                11,
                12,
                13
            ],
            "flow_steps": [
                {
                    "step_id": 11,
                    "step_name": "创建待办事项",
                    "step_description": "待办管理者输入待办任务标题或内容，提交新增任务。",
                    "actor_ids": [
                        3
                    ],
                    "step_type": "actorAction",
                    "input_business_object_ids": [],
                    "output_business_object_ids": [
                        2
                    ],
                    "next_steps": [
                        12
                    ]
                },
                {
                    "step_id": 12,
                    "step_name": "设置截止时间",
                    "step_description": "待办管理者为待办事项设置任务截止时间。",
                    "actor_ids": [
                        3
                    ],
                    "step_type": "actorAction",
                    "input_business_object_ids": [
                        2
                    ],
                    "output_business_object_ids": [
                        2
                    ],
                    "next_steps": [
                        13
                    ]
                },
                {
                    "step_id": 13,
                    "step_name": "判断是否置顶",
                    "step_description": "系统根据用户操作判断该待办事项是否需要置顶显示。",
                    "actor_ids": [],
                    "step_type": "judgment",
                    "input_business_object_ids": [
                        2
                    ],
                    "output_business_object_ids": [],
                    "next_steps": [
                        14,
                        15
                    ]
                },
                {
                    "step_id": 14,
                    "step_name": "置顶重要事项",
                    "step_description": "待办管理者将重要待办事项设置为置顶显示。",
                    "actor_ids": [
                        3
                    ],
                    "step_type": "actorAction",
                    "input_business_object_ids": [
                        2
                    ],
                    "output_business_object_ids": [
                        2
                    ],
                    "next_steps": [
                        15
                    ]
                },
                {
                    "step_id": 15,
                    "step_name": "保存待办事项",
                    "step_description": "系统保存待办事项内容、截止时间、置顶状态和初始完成状态。",
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": [
                        2
                    ],
                    "output_business_object_ids": [
                        2
                    ],
                    "next_steps": [
                        16
                    ]
                },
                {
                    "step_id": 16,
                    "step_name": "标记完成状态",
                    "step_description": "待办管理者在任务完成后将待办事项标记为已完成。",
                    "actor_ids": [
                        3
                    ],
                    "step_type": "actorAction",
                    "input_business_object_ids": [
                        2
                    ],
                    "output_business_object_ids": [
                        2
                    ],
                    "next_steps": [
                        17
                    ]
                },
                {
                    "step_id": 17,
                    "step_name": "更新任务状态",
                    "step_description": "系统更新待办事项完成状态，并刷新待办清单展示。",
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": [
                        2
                    ],
                    "output_business_object_ids": [
                        2
                    ],
                    "next_steps": []
                }
            ]
        },
        {
            "flow_name": "桌面显示控制流程",
            "flow_description": "桌面显示控制者对所有桌面便签执行一键隐藏、恢复显示和常驻显示控制。",
            "feature_ids": [
                16,
                17
            ],
            "flow_steps": [
                {
                    "step_id": 18,
                    "step_name": "选择显示控制操作",
                    "step_description": "桌面显示控制者选择一键隐藏所有便签或恢复显示便签。",
                    "actor_ids": [
                        4
                    ],
                    "step_type": "actorAction",
                    "input_business_object_ids": [
                        3
                    ],
                    "output_business_object_ids": [],
                    "next_steps": [
                        19
                    ]
                },
                {
                    "step_id": 19,
                    "step_name": "判断控制类型",
                    "step_description": "系统判断用户选择的是隐藏所有便签还是恢复显示便签。",
                    "actor_ids": [],
                    "step_type": "judgment",
                    "input_business_object_ids": [
                        3
                    ],
                    "output_business_object_ids": [],
                    "next_steps": [
                        3,
                        4
                    ]
                },
                {
                    "step_id": 20,
                    "step_name": "隐藏所有便签",
                    "step_description": "系统将所有桌面便签设置为隐藏状态，并更新全局显示控制状态。",
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": [
                        1,
                        3
                    ],
                    "output_business_object_ids": [
                        1,
                        3
                    ],
                    "next_steps": []
                },
                {
                    "step_id": 21,
                    "step_name": "恢复显示便签",
                    "step_description": "系统将已隐藏的便签恢复显示，并更新全局显示控制状态。",
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": [
                        1,
                        3
                    ],
                    "output_business_object_ids": [
                        1,
                        3
                    ],
                    "next_steps": []
                }
            ]
        },
        {
            "flow_name": "系统偏好配置流程",
            "flow_description": "系统偏好设置者配置开机常驻、默认便签颜色、默认字体和默认显示样式，供后续新建便签和启动行为使用。",
            "feature_ids": [
                7,
                8,
                15,
                18,
                19
            ],
            "flow_steps": [
                {
                    "step_id": 22,
                    "step_name": "进入偏好设置",
                    "step_description": "系统偏好设置者打开软件设置入口，进入偏好配置界面。",
                    "actor_ids": [
                        5
                    ],
                    "step_type": "actorAction",
                    "input_business_object_ids": [
                        4
                    ],
                    "output_business_object_ids": [],
                    "next_steps": [
                        23
                    ]
                },
                {
                    "step_id": 23,
                    "step_name": "配置开机常驻",
                    "step_description": "系统偏好设置者选择是否启用开机自动运行并保持常驻。",
                    "actor_ids": [
                        5
                    ],
                    "step_type": "actorAction",
                    "input_business_object_ids": [
                        4
                    ],
                    "output_business_object_ids": [
                        4
                    ],
                    "next_steps": [
                        24
                    ]
                },
                {
                    "step_id": 24,
                    "step_name": "配置默认便签样式",
                    "step_description": "系统偏好设置者设置默认颜色、默认字体、默认字号和默认透明度。",
                    "actor_ids": [
                        5
                    ],
                    "step_type": "actorAction",
                    "input_business_object_ids": [
                        4
                    ],
                    "output_business_object_ids": [
                        4
                    ],
                    "next_steps": [
                        25
                    ]
                },
                {
                    "step_id": 25,
                    "step_name": "保存偏好设置",
                    "step_description": "系统保存偏好设置，并将配置用于后续软件启动和新建便签。",
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": [
                        4
                    ],
                    "output_business_object_ids": [
                        4
                    ],
                    "next_steps": []
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