import subprocess
import uuid
import os
from pathlib import Path
from services.scad_builder import build_scad_from_scene
from schemas.export import ExportRequest

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_stl(scene: ExportRequest) -> str:
    scad_code = build_scad_from_scene(scene)
    
    job_id = str(uuid.uuid4())[:8]
    scad_path = OUTPUT_DIR / f"{job_id}.scad"
    stl_path = OUTPUT_DIR / f"{job_id}.stl"
    
    scad_path.write_text(scad_code)
    
    # Run OpenSCAD
    openscad_path = os.getenv("OPENSCAD_PATH", "openscad")
    try:
        subprocess.run(
            [openscad_path, "-o", str(stl_path), str(scad_path)],
            check=True, timeout=30
        )
    except Exception as e:
        print(f"Error running OpenSCAD: {e}")
        # In a real app we'd raise an HTTPException here
        
    return str(stl_path)
