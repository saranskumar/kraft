from schemas.export import ExportRequest

def build_scad_from_scene(scene: ExportRequest) -> str:
    lines = ["$fn = 64;"]
    
    for node in scene.sceneNodes.values():
        part = scene.parts.get(node.partId)
        if not part or not part.visible:
            continue
            
        pos = node.transform.position
        # ThreeJS (Y up) to OpenSCAD (Z up) mapping: (x, y, z) -> (x, z, y)
        # But for simplicity let's stay consistent if the frontend is also using Z up or standard
        # Standard ThreeJS is Y up. OpenSCAD is Z up.
        # Let's map Y to Z and Z to -Y or similar.
        # Actually let's just do a direct mapping for now and let the user adjust if needed, 
        # or do: (x, z, y)
        
        rot = [r * (180.0 / 3.14159) for r in node.transform.rotation]
        scale = node.transform.scale
        
        lines.append("union() {")
        lines.append(f"  translate([{pos[0]}, {pos[2]}, {pos[1]}])")
        lines.append(f"  rotate([{rot[0]}, {rot[2]}, {rot[1]}])")
        lines.append(f"  scale([{scale[0]}, {scale[2]}, {scale[1]}])")
        lines.append("  {")
        
        params = part.params or {}
        if part.kind == "parametric":
            if part.templateId == "chassis_plate_v1":
                l, w, h = params.get("length", 200), params.get("width", 160), params.get("thickness", 3)
                lines.append(f"    cube([{l}, {w}, {h}], center=true);")
                
            elif part.templateId == "motor_mount_n20_v1":
                mw, ml, h = params.get("mount_width", 12), params.get("mount_length", 20), params.get("thickness", 3)
                lines.append(f"    cube([{mw}, {ml}, {h}], center=true);")
                lines.append(f"    translate([{mw/2}, 0, {ml/4}]) cube([1, {ml}, {ml/2}], center=true);")
                lines.append(f"    translate([{-mw/2}, 0, {ml/4}]) cube([1, {ml}, {ml/2}], center=true);")
                
            elif part.templateId == "battery_tray_v1":
                l, w, h, wall = params.get("length", 70), params.get("width", 22), params.get("height", 20), params.get("wall", 2)
                lines.append("    difference() {")
                lines.append(f"      cube([{w}, {l}, {h}], center=true);")
                lines.append(f"      translate([0, 0, {wall}]) cube([{w - wall*2}, {l - wall*2}, {h}], center=true);")
                lines.append("    }")
        elif part.kind == "imported" and part.fileName:
            # Note: This assumes the file is accessible to OpenSCAD
            # In a production app, we'd need to resolve the path correctly
            lines.append(f'    import("{part.fileName}");')
        
        lines.append("  }")
        lines.append("}")
        lines.append("")
        
    return "\n".join(lines)
