from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

from dataclasses_json import dataclass_json, Undefined
from dataclasses_json import DataClassJsonMixin
import inflection

def node_dataclass(cls=None, **kwargs):
    """统一的结点类装饰器，支持传入额外参数覆盖默认配置"""
    def decorator(c):
        # 公共默认配置
        default_config = {
            "undefined": Undefined.EXCLUDE,
            "letter_case": inflection.underscore
        }
        final_config = {**default_config, **kwargs}     # 合并传入的自定义配置
        return dataclass_json(**final_config)(dataclass(c))     # 应用dataclass_json和dataclass装饰器
    if cls is None:
        return decorator
    return decorator(cls)

# 首先定义基础结点类
class BaseNode(DataClassJsonMixin):
    """所有结点的基础类"""
    pass

# 定义枚举类型
class ScopeStatus(str, Enum):
    """功能范围状态枚举"""
    CURRENT = "本期"
    POSTPONED = "暂缓"

class FlowStepType(str, Enum):
    """流程步骤类型枚举"""
    ACTOR_ACTION = "actorAction"
    SYSTEM_ACTION = "systemAction"
    JUDGMENT = "judgment"

class PerceptionKindType(str, Enum):
    """感知槽对应的结点枚举"""
    ACTOR = "角色结点"
    FEATURE = "功能结点"
    SCENARIO = "场景结点"
    FLOW = "流程主结点"

# 角色结点
@node_dataclass
class ActorNode(BaseNode):
    kind: str = field(default="actor", init=False)

    actorId: int
    actorName: str
    actorDescription: str

# 场景结点
@node_dataclass
class ScenarioNode(BaseNode):
    kind: str = field(default="scenario", init=False)

    scenarioId: int
    scenarioName: str
    scenarioContent: str  # 用户故事/场景描述
    featureId: int
    actorId: int

# 范围结点（kano分析结果）
@node_dataclass
class ScopeNode(BaseNode):
    kind: str = field(default="scope", init=False)
    scopeId: int
    scopeStatus: ScopeStatus
    positiveSummary: str
    negativeSummary: str
    reason: str

    positivePictureBase64: Optional[str] = None
    negativePictureBase64: Optional[str] = None

# 功能结点
@node_dataclass
class FeatureNode(BaseNode):
    kind: str = field(default="feature", init=False)

    featureId: int
    featureName: str
    featureDescription: str

    actorIds: List[int] = field(default_factory=list)  # 空数组=没有关联角色
    parentId: Optional[int] = None
    childrenIds: List[int] = field(default_factory=list)      # 空数组表示无子结点，即该结点为叶子

    scenarios: List[ScenarioNode] = field(default_factory=list)      # 空数组表示没有场景
    acceptanceCriteria: List[str] = field(default_factory=list)     # 空数组=没有验收条件

    scope: Optional[ScopeNode] = None

# 业务对象属性结点
@node_dataclass
class BusinessObjectAttributeNode(BaseNode):
    kind: str = field(default="business_object_attribute", init=False)

    businessObjectAttributeId: int
    businessObjectAttributeName: str
    businessObjectAttributeDescription: str
    businessObjectAttributeType: str
    businessObjectAttributeExample: str

# 业务对象主结点
@node_dataclass
class BusinessObjectNode(BaseNode):
    kind: str = field(default="business_object", init=False)

    businessObjectId: int
    businessObjectName: str
    businessObjectDescription: str

    businessObjectAttributes: List[BusinessObjectAttributeNode] = field(default_factory=list)

# 流程步骤结点
@node_dataclass
class FlowStepNode(BaseNode):
    kind: str = field(default="flow_step", init=False)

    stepId: int
    stepName: str
    stepDescription: str

    stepType: FlowStepType

    actorIds: List[int] = field(default_factory=list)  # 空数组=没有
    inputBusinessObjectIds: List[int] = field(default_factory=list)  # 空数组=没有
    outputBusinessObjectIds: List[int] = field(default_factory=list)  # 空数组=没有

    nextStepIds: List[int] = field(default_factory=list)  # 空数组=没有

# 流程主结点
@node_dataclass
class FlowNode(BaseNode):
    kind: str = field(default="flow", init=False)

    flowId: int
    flowName: str
    flowDescription: str

    featureIds: List[int]  # 非空, 步骤必须关联至少一个功能

    flowSteps: List[FlowStepNode] = field(default_factory=list)

# 感知槽结点
@node_dataclass
class PerceptionSlot(BaseNode):
    kind: str = field(default="perception_slot", init=False)

    perceptionSlotId: int
    perceptionKind: PerceptionKindType
    perceptionDescription: str

@node_dataclass
class RequirementSpace(BaseNode):
    """需求空间，包含整个项目的所有需求信息"""
    kind: str = field(default="requirement_space", init=False)

    # 项目基本信息
    projectId: int
    projectName: str
    projectDescription: str
    userRequirements: str

    # 感知槽
    perceptionSlot: Optional[PerceptionSlot] = None  # None表示无感知槽

    # 所有类型的结点集合
    actors: List[ActorNode] = field(default_factory=list)
    features: List[FeatureNode] = field(default_factory=list)
    businessObjects: List[BusinessObjectNode] = field(default_factory=list)
    flows: List[FlowNode] = field(default_factory=list)