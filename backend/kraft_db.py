import sqlite3
import json
import uuid
import time
import os
from typing import List, Dict, Any, Optional

DB_PATH = "kraft.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Projects table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        created_at REAL NOT NULL,
        updated_at REAL NOT NULL,
        last_opened_at REAL NOT NULL,
        scene_data TEXT -- JSON blob of parts, nodes, etc.
    )
    ''')
    
    # Assets table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS assets (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        file_name TEXT NOT NULL,
        file_type TEXT NOT NULL,
        file_path TEXT NOT NULL,
        bounds_data TEXT, -- JSON blob
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
    )
    ''')
    
    # Chat Messages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_messages (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp REAL NOT NULL,
        status TEXT,
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
    )
    ''')
    
    # AI Command Batches table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ai_command_batches (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        prompt TEXT,
        raw_response TEXT,
        applied_commands TEXT, -- JSON blob
        status TEXT,
        error TEXT,
        timestamp REAL NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
    )
    ''')
    
    conn.commit()
    conn.close()

# Initializing the database on import
if not os.path.exists(DB_PATH):
    init_db()
else:
    # Ensure tables exist even if file exists
    init_db()

class ProjectManager:
    @staticmethod
    def create_project(name: str) -> Dict[str, Any]:
        conn = get_db()
        project_id = str(uuid.uuid4())
        now = time.time()
        scene_data = json.dumps({
            "parts": {},
            "sceneNodes": {},
            "selectedNodeIds": []
        })
        
        conn.execute(
            "INSERT INTO projects (id, name, created_at, updated_at, last_opened_at, scene_data) VALUES (?, ?, ?, ?, ?, ?)",
            (project_id, name, now, now, now, scene_data)
        )
        conn.commit()
        conn.close()
        return {
            "id": project_id,
            "name": name,
            "createdAt": now,
            "updatedAt": now,
            "lastOpenedAt": now
        }

    @staticmethod
    def list_projects() -> List[Dict[str, Any]]:
        conn = get_db()
        cursor = conn.execute("SELECT id, name, created_at, updated_at, last_opened_at FROM projects ORDER BY last_opened_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                "id": r["id"],
                "name": r["name"],
                "createdAt": r["created_at"],
                "updatedAt": r["updated_at"],
                "lastOpenedAt": r["last_opened_at"]
            } for r in rows
        ]

    @staticmethod
    def get_project(project_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db()
        cursor = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
            
        # Update last opened
        now = time.time()
        conn.execute("UPDATE projects SET last_opened_at = ? WHERE id = ?", (now, project_id))
        conn.commit()
        
        project = {
            "id": row["id"],
            "name": row["name"],
            "createdAt": row["created_at"],
            "updatedAt": row["updated_at"],
            "lastOpenedAt": now,
            "sceneData": json.loads(row["scene_data"]) if row["scene_data"] else None
        }
        conn.close()
        return project

    @staticmethod
    def update_project(project_id: str, data: Dict[str, Any]) -> bool:
        conn = get_db()
        now = time.time()
        
        # Build update query
        fields = []
        params = []
        
        if "name" in data:
            fields.append("name = ?")
            params.append(data["name"])
            
        if "sceneData" in data:
            fields.append("scene_data = ?")
            params.append(json.dumps(data["sceneData"]))
            
        if not fields:
            conn.close()
            return False
            
        fields.append("updated_at = ?")
        params.append(now)
        params.append(project_id)
        
        query = f"UPDATE projects SET {', '.join(fields)} WHERE id = ?"
        conn.execute(query, params)
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete_project(project_id: str) -> bool:
        conn = get_db()
        conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def add_chat_message(project_id: str, role: str, content: str, status: str = None) -> Dict[str, Any]:
        conn = get_db()
        msg_id = str(uuid.uuid4())
        now = time.time()
        conn.execute(
            "INSERT INTO chat_messages (id, project_id, role, content, timestamp, status) VALUES (?, ?, ?, ?, ?, ?)",
            (msg_id, project_id, role, content, now, status)
        )
        conn.commit()
        conn.close()
        return {
            "id": msg_id,
            "role": role,
            "content": content,
            "timestamp": now,
            "status": status
        }

    @staticmethod
    def get_chat_history(project_id: str) -> List[Dict[str, Any]]:
        conn = get_db()
        cursor = conn.execute("SELECT * FROM chat_messages WHERE project_id = ? ORDER BY timestamp ASC", (project_id,))
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                "id": r["id"],
                "role": r["role"],
                "content": r["content"],
                "timestamp": r["timestamp"],
                "status": r["status"]
            } for r in rows
        ]

    @staticmethod
    def add_asset(project_id: str, file_name: str, file_type: str, file_path: str, bounds_data: Dict[str, Any] = None) -> Dict[str, Any]:
        conn = get_db()
        asset_id = str(uuid.uuid4())
        bounds_json = json.dumps(bounds_data) if bounds_data else None
        conn.execute(
            "INSERT INTO assets (id, project_id, file_name, file_type, file_path, bounds_data) VALUES (?, ?, ?, ?, ?, ?)",
            (asset_id, project_id, file_name, file_type, file_path, bounds_json)
        )
        conn.commit()
        conn.close()
        return {
            "id": asset_id,
            "fileName": file_name,
            "fileType": file_type,
            "filePath": file_path,
            "bounds": bounds_data
        }

    @staticmethod
    def get_assets(project_id: str) -> List[Dict[str, Any]]:
        conn = get_db()
        cursor = conn.execute("SELECT * FROM assets WHERE project_id = ?", (project_id,))
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                "id": r["id"],
                "fileName": r["file_name"],
                "fileType": r["file_type"],
                "filePath": r["file_path"],
                "bounds": json.loads(r["bounds_data"]) if r["bounds_data"] else None
            } for r in rows
        ]
