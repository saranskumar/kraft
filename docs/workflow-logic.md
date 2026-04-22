# Workflow Logic

## AI Transaction Flow
1. **Input**: User sends natural language in the Chat Panel.
2. **Contextualization**: The system bundles the current `sceneNodes` and `parts` state.
3. **Generation**: Backend calls Gemini with the prompt and context.
4. **Validation**: AI returns a JSON array of `AICommand` objects.
5. **Execution**: `editorStore.ts` applies the commands to the state.
6. **Logging**: Success/Error results are pushed to the Bottom Panel.

## Geometry Export Flow
1. **Trigger**: User clicks "Export STL".
2. **Assembly**: Frontend sends the full scene graph to the backend.
3. **Translation**: `scad_builder.py` maps Three.js transforms to SCAD syntax.
4. **Execution**: System runs `openscad` CLI to render the `.scad` file to `.stl`.
5. **Delivery**: Backend returns the STL binary for client download.

## History System (Undo/Redo)
- **Snapshotting**: Triggered only after discrete user actions (Gizmo release, Property change commit).
- **Store**: `editorStore.ts` maintains a `history` (stack) and `future` (queue) of scene snapshots.
