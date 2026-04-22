# API Contracts

## AI Service
### POST `/api/ai/command`
Generates structured scene commands from natural language.
- **Request**: `{ "prompt": string, "context": { "nodes": SceneNode[], "parts": Part[] } }`
- **Response**: `{ "commands": AICommand[], "explanation": string }`

## Export Service
### POST `/api/export/stl`
Generates and downloads an STL assembly from the scene graph.
- **Request**: `{ "nodes": SceneNode[], "parts": Part[] }`
- **Response**: STL Binary File

## Template Service
### GET `/api/templates`
Retrieves the list of available robotic parametric templates.
- **Response**: `PartTemplate[]`
