from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from schemas.export import ExportRequest
from services.geometry_engine import generate_export
import os
import json

router = APIRouter()

@router.post("/export/stl")
async def export_stl(request: ExportRequest):
    try:
        output_path, warnings = generate_export(request)
        if os.path.exists(output_path):
            headers = {}
            if warnings:
                # Store warnings in a custom header
                headers["X-Export-Warnings"] = json.dumps(warnings)
                
            return FileResponse(
                output_path, 
                media_type="application/octet-stream", 
                filename=os.path.basename(output_path),
                headers=headers
            )
        raise HTTPException(status_code=500, detail="Failed to generate export file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
