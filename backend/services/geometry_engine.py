import subprocess
import uuid
import os
import trimesh
import numpy as np
from pathlib import Path
from services.scad_builder import build_scad_from_scene
from schemas.export import ExportRequest

OUTPUT_DIR = Path("output")
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_export(request: ExportRequest) -> tuple[str, list[str]]:
    job_id = str(uuid.uuid4())[:8]
    ext = request.format.lower() if request.format else "stl"
    mode = request.exportMode or "full"
    
    # Valid extensions
    valid_exts = ["stl", "obj", "scad", "off", "amf", "3mf"]
    if ext not in valid_exts:
        ext = "stl"

    # Step 1: Identify parametric vs imported nodes
    parametric_nodes = {}
    imported_nodes = []
    warnings = []
    
    for node_id, node in request.sceneNodes.items():
        part = request.parts.get(node.partId)
        if not part or not part.visible:
            continue
        if part.kind == "parametric":
            parametric_nodes[node_id] = node
        elif part.kind == "imported":
            imported_nodes.append((node, part))

    # Step 2: Handle Parametric Parts via OpenSCAD
    parametric_stl_path = None
    if parametric_nodes:
        # We need a sub-request for scad_builder
        sub_request = ExportRequest(
            parts=request.parts,
            sceneNodes=parametric_nodes,
            format="stl"
        )
        scad_code = build_scad_from_scene(sub_request)
        scad_path = OUTPUT_DIR / f"{job_id}_para.scad"
        scad_path.write_text(scad_code)
        
        if ext == "scad" and mode == "parametric":
            if imported_nodes:
                warnings.append("Imported meshes excluded in parametric mode.")
            return (str(scad_path), warnings)
            
        parametric_stl_path = OUTPUT_DIR / f"{job_id}_para.stl"
        openscad_path = os.getenv("OPENSCAD_PATH", "openscad").strip('"\'')
        
        try:
            subprocess.run(
                [openscad_path, "-o", str(parametric_stl_path), str(scad_path)],
                check=True, timeout=30, capture_output=True, text=True
            )
        except Exception as e:
            print(f"OpenSCAD Error: {e}")
            # If it fails, we continue without parametric or raise if mode is parametric
            if mode == "parametric":
                raise Exception(f"OpenSCAD failed: {str(e)}")
    
    # Step 3: Handle Mode logic
    if mode == "parametric" or not imported_nodes:
        if parametric_stl_path and parametric_stl_path.exists():
            final_path = OUTPUT_DIR / f"{job_id}.{ext}"
            parametric_stl_path.rename(final_path)
            if imported_nodes:
                warnings.append("Imported meshes excluded in parametric mode.")
            return (str(final_path), warnings)
        else:
            raise Exception("No parametric geometry to export in parametric mode.")

    # Step 4: Full Assembly Merge (Trimesh)
    meshes = []
    
    # Add parametric mesh
    if parametric_stl_path and parametric_stl_path.exists():
        p_mesh = trimesh.load(str(parametric_stl_path))
        meshes.append(p_mesh)

    # Add imported meshes
    for node, part in imported_nodes:
        if not part.fileName:
            continue
            
        asset_path = UPLOAD_DIR / part.fileName
        if not asset_path.exists():
            msg = f"Asset not found: {asset_path}"
            print(msg)
            warnings.append(msg)
            continue
            
        try:
            m = trimesh.load(str(asset_path))
            
            # Apply Transforms
            # We must follow the same mapping as scad_builder: (X, Y, Z) -> (X, Z, Y)
            pos = node.transform.position
            rot = node.transform.rotation # radians
            scale = node.transform.scale
            
            # Create transformation matrix
            # 1. Scale
            S = np.diag([scale[0], scale[2], scale[1], 1.0])
            
            # 2. Rotate (OpenSCAD style: X, then Z, then Y?? No, scad_builder uses rotate([x, z, y]))
            # Three.js uses XYZ Euler.
            # In scad_builder: rotate([rot[0], rot[2], rot[1]])
            # This is a bit complex in Trimesh. Let's use Euler angles.
            # OpenSCAD rotate([a, b, c]) is rotate(c, [0,0,1]) * rotate(b, [0,1,0]) * rotate(a, [1,0,0])
            R = trimesh.transformations.euler_matrix(rot[0], rot[2], rot[1], 'rxyz')
            
            # 3. Translate
            T = trimesh.transformations.translation_matrix([pos[0], pos[2], pos[1]])
            
            # Combined: T * R * S
            M = T @ R @ S
            m.apply_transform(M)
            
            meshes.append(m)
        except Exception as e:
            msg = f"Error loading/transforming mesh {part.fileName}: {e}"
            print(msg)
            warnings.append("Some parts could not be merged: " + part.fileName)

    if not meshes:
        raise Exception("No geometry found to merge.")

    # Step 5: Concatenate and Export
    final_mesh = trimesh.util.concatenate(meshes)
    output_path = OUTPUT_DIR / f"{job_id}.{ext}"
    final_mesh.export(str(output_path))
    
    # Cleanup temp files
    if parametric_stl_path and parametric_stl_path.exists():
        parametric_stl_path.unlink()
    
    return (str(output_path), warnings)
