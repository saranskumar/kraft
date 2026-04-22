from fastapi import APIRouter, HTTPException
from schemas.ai import AICommandRequest, AICommandResponse
from services.ai_service import generate_commands

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/command", response_model=AICommandResponse)
async def get_ai_command(request: AICommandRequest):
    try:
        commands = generate_commands(request.prompt, request.scene, request.selection)
        return {"commands": commands}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
