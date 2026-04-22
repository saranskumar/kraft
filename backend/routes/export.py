from fastapi import APIRouter
from fastapi.responses import FileResponse
from schemas.export import ExportRequest
from services.geometry_engine import generate_stl
import os

router = APIRouter()

@router.post("/export/stl")
async def export_stl(request: ExportRequest):
    stl_path = generate_stl(request)
    if os.path.exists(stl_path):
        return FileResponse(
            stl_path, 
            media_type="application/octet-stream", 
            filename=os.path.basename(stl_path)
        )
    return {"error": "Failed to generate STL"}
