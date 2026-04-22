from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union

class AICommandRequest(BaseModel):
    prompt: str
    scene: Dict[str, Any]
    selection: List[str]
    history: Optional[List[Dict[str, str]]] = None

class AICommand(BaseModel):
    action: str
    target: Optional[str] = None
    targets: Optional[List[str]] = None
    param: Optional[str] = None
    mode: Optional[str] = None
    value: Optional[float] = None
    type: Optional[str] = None
    values: Optional[List[float]] = None
    templateId: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    position: Optional[List[float]] = None
    axis: Optional[str] = None

class AICommandResponse(BaseModel):
    commands: List[AICommand]
