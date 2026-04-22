import os
import json
from google import genai
from google.genai import types
from typing import List, Dict, Any

SYSTEM_PROMPT = """
You are a CAD command planner for a parametric 3D editor called Kraft CAD.

RULES:
- ONLY return valid JSON matching the output schema below.
- DO NOT add explanations, comments, or markdown.
- DO NOT generate geometry descriptions.
- Use ONLY the node IDs and part IDs present in the provided scene.
- If "selection" is non-empty, target those nodes first.
- If "selection" is empty, apply to all nodes or pick the most appropriate one.

COORDINATE SYSTEM: Three.js (Y-up). Units are millimetres.

AVAILABLE TEMPLATES:
- "chassis_plate_v1" (params: length, width, thickness)
- "motor_mount_n20_v1" (params: mount_width, mount_length, thickness)
- "battery_tray_v1" (params: width, length, height, wall)

SUPPORTED ACTIONS:
1. update_param     → { "action": "update_param", "target": "<nodeId>", "param": "<paramName>", "mode": "set|delta", "value": <number> }
2. transform        → { "action": "transform", "target": "<nodeId>", "type": "translate|rotate|scale", "values": [x, y, z], "mode": "absolute|delta" }
3. add_part         → { "action": "add_part", "templateId": "<id>", "params": { ... }, "position": [x, y, z] }
4. duplicate_part    → { "action": "duplicate_part", "target": "<nodeId>" }
5. delete_part      → { "action": "delete_part", "target": "<nodeId>" }
6. align_center     → { "action": "align_center", "targets": ["<nodeId>", ...], "axis": "x|y|z" }
7. mirror_part      → { "action": "mirror_part", "target": "<nodeId>", "axis": "x|y|z" }
8. offset           → { "action": "offset", "source": "<nodeId>", "target": "<nodeId>", "axis": "x|y|z", "value": <distance> }
9. snap_to_face     → { "action": "snap_to_face", "source": "<nodeId>", "target": "<nodeId>", "face": "top|bottom|left|right|front|back" }
10. distribute       → { "action": "distribute", "targets": ["<id>", ...], "axis": "x|y|z" }
11. pattern_duplicate → { "action": "pattern_duplicate", "target": "<id>", "axis": "x|y|z", "count": <num>, "spacing": <mm> }

OUTPUT SCHEMA (strict):
{
  "commands": [ { ...one of the above... } ]
}
"""

def generate_commands(prompt: str, scene: Dict[str, Any], selection: List[str]) -> List[Dict[str, Any]]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment")
    
    # Initialize the new Gemini 3 Client
    client = genai.Client(api_key=api_key)

    user_message = f"""
Scene (JSON):
{json.dumps(scene, indent=2)}

Current selection (node IDs):
{json.dumps(selection)}

User instruction:
"{prompt}"

Return ONLY a JSON object with a "commands" array.
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=SYSTEM_PROMPT + "\n\n" + user_message,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.7,
        )
    )

    try:
        text = response.text.strip()
        # Clean up possible markdown fences
        if text.startswith("```"):
            lines = text.splitlines()
            if lines[0].startswith("```json"):
                text = "\n".join(lines[1:-1])
            else:
                text = "\n".join(lines[1:-1])
        
        data = json.loads(text)
        return data.get("commands", [])
    except (json.JSONDecodeError, ValueError) as e:
        print(f"[AI Service] Failed to parse response: {e}")
        print(f"[AI Service] Raw response: {response.text[:500]}")
        return []
