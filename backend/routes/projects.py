from fastapi import APIRouter, HTTPException, Body, UploadFile, File
from typing import List, Dict, Any, Optional
from kraft_db import ProjectManager
import shutil
import os

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("")
async def create_project(data: Dict[str, str] = Body(...)):
    name = data.get("name", "New Project")
    return ProjectManager.create_project(name)

@router.get("")
async def list_projects():
    return ProjectManager.list_projects()

@router.get("/{project_id}")
async def get_project(project_id: str):
    project = ProjectManager.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}")
async def update_project(project_id: str, data: Dict[str, Any] = Body(...)):
    success = ProjectManager.update_project(project_id, data)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update project")
    return {"status": "success"}

@router.delete("/{project_id}")
async def delete_project(project_id: str):
    ProjectManager.delete_project(project_id)
    return {"status": "success"}

@router.get("/{project_id}/chat")
async def get_chat_history(project_id: str):
    return ProjectManager.get_chat_history(project_id)

@router.post("/{project_id}/chat")
async def add_chat_message(project_id: str, data: Dict[str, Any] = Body(...)):
    role = data.get("role")
    content = data.get("content")
    status = data.get("status")
    if not role or not content:
        raise HTTPException(status_code=400, detail="Role and content required")
    return ProjectManager.add_chat_message(project_id, role, content, status)

@router.post("/{project_id}/assets")
async def upload_asset(project_id: str, file: UploadFile = File(...)):
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
        
    file_path = os.path.join("uploads", f"{project_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    file_type = file.filename.split(".")[-1].lower()
    return ProjectManager.add_asset(project_id, file.filename, file_type, file_path)

@router.get("/{project_id}/assets")
async def list_assets(project_id: str):
    return ProjectManager.get_assets(project_id)
