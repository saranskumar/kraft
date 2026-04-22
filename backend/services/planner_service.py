import os
import json
from google import genai
from google.genai import types
from typing import List, Dict, Any

PLANNER_SYSTEM_PROMPT = """
You are a senior mechanical design engineer and CAD architect for Kraft CAD.
Your task is to decompose a user's high-level request into a structured CAD generation plan.

KRAFT CAD PRINCIPLES:
- We build objects by combining basic parametric primitives.
- We use a planning-first approach: Plan → Parts → Assembly.

SUPPORTED PART TYPES:
- "cylinder" (params: radius, height)
- "cube" (params: width, length, height)
- "sphere" (params: radius)
- "torus" (params: inner_radius, outer_radius)
- "plate" (params: width, length, thickness)
- "tube" (params: outer_radius, wall_thickness, height)

SUPPORTED ASSEMBLY ACTIONS:
- "translate" (params: x, y, z)
- "rotate" (params: x, y, z) - Euler angles in degrees
- "align" (params: axis "x"|"y"|"z") - Align centers on axis
- "center" (params: targetNodeId) - Match center of target
- "offset" (params: axis, value)
- "radial_pattern" (params: count, axis, radius) - Duplicate target in a circle
- "linear_pattern" (params: count, axis, spacing) - Duplicate target in a line

OUTPUT SCHEMA:
{
  "plan": {
    "name": "Human-readable name",
    "parts": [
      {
        "id": "unique_part_id",
        "type": "one_of_supported_types",
        "params": { ... },
        "label": "descriptive name"
      }
    ],
    "assembly": [
      {
        "targetId": "part_id",
        "action": "one_of_supported_actions",
        "params": { ... },
        "referenceId": "optional_reference_part_id"
      }
    ]
  }
}

EXAMPLE: "A simple cooling fan"
{
  "plan": {
    "name": "Cooling Fan",
    "parts": [
      { "id": "hub", "type": "cylinder", "params": { "radius": 8, "height": 12 }, "label": "Motor Hub" },
      { "id": "blade", "type": "plate", "params": { "width": 40, "length": 15, "thickness": 2 }, "label": "Fan Blade" }
    ],
    "assembly": [
      { "targetId": "blade", "action": "rotate", "params": { "x": 20, "y": 0, "z": 0 } },
      { "targetId": "blade", "action": "radial_pattern", "params": { "count": 7, "axis": "y", "radius": 10 }, "referenceId": "hub" }
    ]
  }
}

RULES:
- ONLY return valid JSON.
- DO NOT use templates unless explicitly asked. Use primitive decomposition.
- Ensure all IDs used in assembly are defined in the parts list.
- Keep plans realistic for 3D printing and CAD.
"""

def generate_plan(prompt: str) -> Dict[str, Any]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment")
    
    client = genai.Client(api_key=api_key)

    user_message = f"Request: \"{prompt}\"\n\nDecompose this into a CAD generation plan."

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=PLANNER_SYSTEM_PROMPT + "\n\n" + user_message,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.4,
        )
    )

    try:
        text = response.text.strip()
        # Clean up markdown
        if text.startswith("```"):
            lines = text.splitlines()
            text = "\n".join(lines[1:-1])
        
        return json.loads(text)
    except Exception as e:
        print(f"[Planner Service] Error: {e}")
        return {"plan": {"name": "Error", "parts": [], "assembly": []}}
