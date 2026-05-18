flows_perceive_prompt = """
# 角色
你是一个善于设计项目流程的软件设计师。

# 任务
1. 分析用户用自然语言描述的项目需求、目标系统参与者（用户）、目标系统能力（features tree）与当前整理出的系统流程。
2. 判断是否需要补充系统流程（注意不是流程步骤，是流程）。若需要，则描述需要补充什么，为何需要补充，如何补充；若不需要，则输出不需要。
3. 按照下方规定输出格式输出补充系统流程的原因。

# 用户需求
{{user_initial_requirements}}

# 参与者（用户）
{{actors}}

# 系统能力（features tree）
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
{轻量化桌面悬浮便签 + 待办整合软件，可新建多个独立便签贴在桌面任意位置，支持文字编辑、颜色分类、字体调整；自带待办清单功能，可设置任务截止时间、已完成标记、置顶重要事项，支持开机常驻、透明化背景、一键隐藏所有便签，适合学生、上班族记录临时灵感、日程、琐事。}
### 参与者（用户）
{
    "actors": [
        {
            "actor_id": "A001",
            "actor_name": "普通用户",
            "actor_description": "使用本软件进行便签记录、待办任务管理的学生、上班族等个人使用者"
        }
    ]
}
### 系统能力（features tree）
{
    "features": [
        {
            "feature_id": "F001",
            "feature_name": "便签管理",
            "feature_description": "对桌面悬浮便签进行创建、编辑、样式调整及删除等全生命周期管理",
            "actor_ids": ["A001"],
            "business_object_ids": ["B001"],
            "priority": "P0",
            "parent_id": ""
        },
        {
            "feature_id": "F001-001",
            "feature_name": "新建独立便签",
            "feature_description": "支持创建多个相互独立的悬浮便签，可拖动至桌面任意位置摆放",
            "actor_ids": ["A001"],
            "business_object_ids": ["B001"],
            "priority": "P0",
            "parent_id": "F001"
        },
        {
            "feature_id": "F001-002",
            "feature_name": "便签文字编辑",
            "feature_description": "支持对便签内容进行文字输入、修改、删除等基础编辑操作",
            "actor_ids": ["A001"],
            "business_object_ids": ["B001"],
            "priority": "P0",
            "parent_id": "F001"
        },
        {
            "feature_id": "F001-003",
            "feature_name": "便签颜色分类",
            "feature_description": "支持为不同便签设置不同背景颜色，用于分类区分不同主题的内容",
            "actor_ids": ["A001"],
            "business_object_ids": ["B001"],
            "priority": "P1",
            "parent_id": "F001"
        },
        {
            "feature_id": "F001-004",
            "feature_name": "便签字体调整",
            "feature_description": "支持调整便签内文字的字体、字号、颜色等显示样式",
            "actor_ids": ["A001"],
            "business_object_ids": ["B001"],
            "priority": "P1",
            "parent_id": "F001"
        },
        {
            "feature_id": "F001-005",
            "feature_name": "便签删除",
            "feature_description": "支持删除不再需要的悬浮便签",
            "actor_ids": ["A001"],
            "business_object_ids": ["B001"],
            "priority": "P0",
            "parent_id": "F001"
        },
        {
            "feature_id": "F002",
            "feature_name": "待办清单管理",
            "feature_description": "对待办任务进行创建、状态管理、优先级设置及删除等操作",
            "actor_ids": ["A001"],
            "business_object_ids": ["B002"],
            "priority": "P0",
            "parent_id": ""
        },
        {
            "feature_id": "F002-001",
            "feature_name": "新建待办任务",
            "feature_description": "支持创建待办任务条目，输入任务具体内容",
            "actor_ids": ["A001"],
            "business_object_ids": ["B002"],
            "priority": "P0",
            "parent_id": "F002"
        },
        {
            "feature_id": "F002-002",
            "feature_name": "设置任务截止时间",
            "feature_description": "支持为待办任务设置具体的截止日期和时间",
            "actor_ids": ["A001"],
            "business_object_ids": ["B002"],
            "priority": "P1",
            "parent_id": "F002"
        },
        {
            "feature_id": "F002-003",
            "feature_name": "任务已完成标记",
            "feature_description": "支持将已完成的待办任务标记为完成状态，区分未完成任务",
            "actor_ids": ["A001"],
            "business_object_ids": ["B002"],
            "priority": "P0",
            "parent_id": "F002"
        },
        {
            "feature_id": "F002-004",
            "feature_name": "重要任务置顶",
            "feature_description": "支持将重要的待办任务置顶显示，优先提醒用户处理",
            "actor_ids": ["A001"],
            "business_object_ids": ["B002"],
            "priority": "P1",
            "parent_id": "F002"
        },
        {
            "feature_id": "F002-005",
            "feature_name": "待办任务删除",
            "feature_description": "支持删除不再需要的待办任务条目",
            "actor_ids": ["A001"],
            "business_object_ids": ["B002"],
            "priority": "P0",
            "parent_id": "F002"
        },
        {
            "feature_id": "F003",
            "feature_name": "系统设置与便捷操作",
            "feature_description": "提供软件系统配置及提升使用效率的便捷操作功能",
            "actor_ids": ["A001"],
            "business_object_ids": ["B003"],
            "priority": "P1",
            "parent_id": ""
        },
        {
            "feature_id": "F003-001",
            "feature_name": "开机常驻启动",
            "feature_description": "支持设置软件随系统开机自动启动并常驻后台运行",
            "actor_ids": ["A001"],
            "business_object_ids": ["B003"],
            "priority": "P1",
            "parent_id": "F003"
        },
        {
            "feature_id": "F003-002",
            "feature_name": "便签背景透明化",
            "feature_description": "支持调整便签的背景透明度，减少对桌面其他内容的遮挡",
            "actor_ids": ["A001"],
            "business_object_ids": ["B001", "B003"],
            "priority": "P1",
            "parent_id": "F003"
        },
        {
            "feature_id": "F003-003",
            "feature_name": "一键隐藏所有便签",
            "feature_description": "支持通过快捷键或按钮一键隐藏/显示所有悬浮便签与待办清单",
            "actor_ids": ["A001"],
            "business_object_ids": ["B001", "B002", "B003"],
            "priority": "P1",
            "parent_id": "F003"
        },
        {
            "feature_id": "F003-004",
            "feature_name": "数据自动保存",
            "feature_description": "系统自动定时保存用户创建的便签与待办数据，防止数据意外丢失",
            "actor_ids": [],
            "business_object_ids": ["B001", "B002", "B003"],
            "priority": "P0",
            "parent_id": "F003"
        }
    ]
}
### 当前整理出的流程
{
    "flows": [
        {
            "flow_id": "FL001",
            "flow_name": "便签全生命周期管理流程",
            "flow_description": "用户对桌面悬浮便签进行创建、编辑、样式调整、删除等全生命周期操作，系统自动保存便签数据", 
            "flow_steps": [
                {
                    "step_id": "FL001-001",
                    "step_name": "新建独立便签",
                    "step_description": "用户触发新建便签操作，系统根据默认系统配置创建一个新的悬浮便签，用户可拖动至桌面任意位置",
                    "feature_ids": ["F001-001"],
                    "actor_ids": ["A001"],
                    "step_type": "actorAction",
                    "input_business_object_ids": ["B003"],
                    "output_business_object_ids": ["B001"]
                },
                {
                    "step_id": "FL001-002",
                    "step_name": "便签文字编辑",
                    "step_description": "用户在便签内进行文字输入、修改、删除等基础编辑操作",
                    "feature_ids": ["F001-002"],
                    "actor_ids": ["A001"],
                    "step_type": "actorAction",
                    "input_business_object_ids": ["B001"],
                    "output_business_object_ids": ["B001"]
                },
                {
                    "step_id": "FL001-003",
                    "step_name": "便签颜色分类设置",
                    "step_description": "用户为便签选择不同的背景颜色，用于分类区分不同主题的内容",
                    "feature_ids": ["F001-003"],
                    "actor_ids": ["A001"],
                    "step_type": "actorAction",
                    "input_business_object_ids": ["B001"],
                    "output_business_object_ids": ["B001"]
                },
                {
                    "step_id": "FL001-004",
                    "step_name": "便签字体调整",
                    "step_description": "用户调整便签内文字的字体、字号、颜色等显示样式",
                    "feature_ids": ["F001-004"],
                    "actor_ids": ["A001"],
                    "step_type": "actorAction",
                    "input_business_object_ids": ["B001"],
                    "output_business_object_ids": ["B001"]
                },
                {
                    "step_id": "FL001-005",
                    "step_name": "便签背景透明度调整",
                    "step_description": "用户调整便签的背景透明度，减少对桌面其他内容的遮挡，同时更新系统默认透明度配置",
                    "feature_ids": ["F003-002"],
                    "actor_ids": ["A001"],
                    "step_type": "actorAction",
                    "input_business_object_ids": ["B001", "B003"],
                    "output_business_object_ids": ["B001", "B003"]
                },
                {
                    "step_id": "FL001-006",
                    "step_name": "便签删除",
                    "step_description": "用户触发删除操作，系统移除指定的悬浮便签",
                    "feature_ids": ["F001-005"],
                    "actor_ids": ["A001"],
                    "step_type": "actorAction",
                    "input_business_object_ids": ["B001"],
                    "output_business_object_ids": []
                },
                {
                    "step_id": "FL001-007",
                    "step_name": "便签数据自动保存",
                    "step_description": "系统按照设定的时间间隔自动保存用户创建或修改的便签数据，防止数据意外丢失",
                    "feature_ids": ["F003-004"],
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": ["B001"],
                    "output_business_object_ids": ["B001"]
                }
            ]
        },
        {
            "flow_id": "FL002",
            "flow_name": "待办任务全生命周期管理流程",
            "flow_description": "用户对待办任务进行创建、截止时间设置、完成标记、置顶、删除等操作，系统自动保存待办数据", 
            "flow_steps": [
                {
                    "step_id": "FL002-001",
                    "step_name": "新建待办任务",
                    "step_description": "用户触发新建待办任务操作，输入任务具体内容，系统创建新的待办任务条目",
                    "feature_ids": ["F002-001"],
                    "actor_ids": ["A001"],
                    "step_type": "actorAction",
                    "input_business_object_ids": [],
                    "output_business_object_ids": ["B002"]
                },
                {
                    "step_id": "FL002-002",
                    "step_name": "设置任务截止时间",
                    "step_description": "用户为待办任务设置具体的截止日期和时间",
                    "feature_ids": ["F002-002"],
                    "actor_ids": ["A001"],
                    "step_type": "actorAction",
                    "input_business_object_ids": ["B002"],
                    "output_business_object_ids": ["B002"]
                },
                {
                    "step_id": "FL002-003",
                    "step_name": "任务已完成标记",
                    "step_description": "用户将已完成的待办任务标记为完成状态，系统记录完成时间",
                    "feature_ids": ["F002-003"],
                    "actor_ids": ["A001"],
                    "step_type": "actorAction",
                    "input_business_object_ids": ["B002"],
                    "output_business_object_ids": ["B002"]
                },
                {
                    "step_id": "FL002-004",
                    "step_name": "重要任务置顶",
                    "step_description": "用户将重要的待办任务置顶显示，优先提醒用户处理",
                    "feature_ids": ["F002-004"],
                    "actor_ids": ["A001"],
                    "step_type": "actorAction",
                    "input_business_object_ids": ["B002"],
                    "output_business_object_ids": ["B002"]
                },
                {
                    "step_id": "FL002-005",
                    "step_name": "待办任务删除",
                    "step_description": "用户触发删除操作，系统移除指定的待办任务条目",
                    "feature_ids": ["F002-005"],
                    "actor_ids": ["A001"],
                    "step_type": "actorAction",
                    "input_business_object_ids": ["B002"],
                    "output_business_object_ids": []
                },
                {
                    "step_id": "FL002-006",
                    "step_name": "待办数据自动保存",
                    "step_description": "系统按照设定的时间间隔自动保存用户创建或修改的待办任务数据，防止数据意外丢失",
                    "feature_ids": ["F003-004"],
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": ["B002"],
                    "output_business_object_ids": ["B002"]
                },
            ]
        },
        {
            "flow_id": "FL003",
            "flow_name": "系统配置与便捷操作流程",
            "flow_description": "用户进行软件全局系统配置及使用便捷操作，系统应用配置并执行对应操作，自动保存配置数据", 
            "flow_steps": [
                {
                    "step_id": "FL003-001",
                    "step_name": "设置开机常驻启动",
                    "step_description": "用户设置软件随系统开机自动启动并常驻后台运行",
                    "feature_ids": ["F003-001"],
                    "actor_ids": ["A001"],
                    "step_type": "actorAction",
                    "input_business_object_ids": ["B003"],
                    "output_business_object_ids": ["B003"]
                },
                {
                    "step_id": "FL003-002",
                    "step_name": "一键隐藏/显示所有便签与待办",
                    "step_description": "用户通过快捷键或按钮触发一键隐藏/显示操作，系统切换所有悬浮便签与待办清单的显示状态",
                    "feature_ids": ["F003-003"],
                    "actor_ids": ["A001"],
                    "step_type": "actorAction",
                    "input_business_object_ids": ["B001", "B002", "B003"],
                    "output_business_object_ids": ["B001", "B002", "B003"]
                },
                {
                    "step_id": "FL003-003",
                    "step_name": "系统配置自动保存",
                    "step_description": "系统按照设定的时间间隔自动保存用户修改的系统配置数据，防止配置丢失",
                    "feature_ids": ["F003-004"],
                    "actor_ids": [],
                    "step_type": "systemAction",
                    "input_business_object_ids": ["B003"],
                    "output_business_object_ids": ["B003"]
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