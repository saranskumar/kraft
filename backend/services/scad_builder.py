from schemas.export import ExportRequest, Part, SceneNode

def build_scad_from_scene(scene: ExportRequest) -> str:
    lines = []
    
    # Simple definition for primitives
    for node_id, node in scene.sceneNodes.items():
        part = scene.parts.get(node.partId)
        if not part or not part.visible:
            continue
            
        pos = node.transform.position
        # OpenSCAD rotation is in degrees, but we might have radians from threejs
        # Assuming radians, convert to degrees for OpenSCAD
        rot = [r * (180.0 / 3.14159265359) for r in node.transform.rotation]
        scale = node.transform.scale
        
        # OpenSCAD translation & rotation block
        lines.append(f"translate([{pos[0]}, {pos[1]}, {pos[2]}])")
        lines.append(f"rotate([{rot[0]}, {rot[1]}, {rot[2]}])")
        lines.append(f"scale([{scale[0]}, {scale[1]}, {scale[2]}])")
        
        if part.type == "primitive_box":
            w = part.params.get("width", 10)
            d = part.params.get("depth", 10)
            h = part.params.get("height", 10)
            # ThreeJS box is centered, OpenSCAD cube(center=true)
            lines.append(f"cube([{w}, {h}, {d}], center=true);")
            
        elif part.type == "primitive_cylinder":
            r = part.params.get("radius", 5)
            h = part.params.get("height", 10)
            # ThreeJS cylinder is centered
            lines.append(f"cylinder(h={h}, r1={r}, r2={r}, center=true, $fn=32);")
            
        lines.append("") # Empty line between parts

    return "\n".join(lines)
