from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class Part(BaseModel):
    id: str
    type: str
    templateId: str
    params: Dict[str, Any]
    material: Optional[str] = None
    visible: bool = True
    locked: bool = False

class SceneNodeTransform(BaseModel):
    position: List[float]
    rotation: List[float]
    scale: List[float]

class SceneNode(BaseModel):
    id: str
    partId: str
    parentId: Optional[str] = None
    transform: SceneNodeTransform

class ExportRequest(BaseModel):
    parts: Dict[str, Part]
    sceneNodes: Dict[str, SceneNode]
