from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class Part(BaseModel):
    id: str
    kind: str # "parametric" or "imported"
    templateId: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    fileName: Optional[str] = None
    sourceType: Optional[str] = None
    sourceUrl: Optional[str] = None
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
    format: Optional[str] = "stl"
    exportMode: Optional[str] = "full" # "parametric" | "full"
    projectId: Optional[str] = None
