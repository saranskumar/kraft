# Architectural Decisions: Kraft CAD v2

## ADR-001: Trimesh for Geometry Merging
**Decision**: Use `trimesh` (Python) for the unified export pipeline.
**Rationale**: Handles heterogeneous mesh formats (STL, OBJ, 3MF) and provides robust matrix-based transformations for assembly alignment.

## ADR-002: Coordinate System Mapping
**Decision**: Standardize on Y-up for Viewport (Three.js) and Z-up for Export (OpenSCAD/3D Printing).
**Rationale**: Ensures compatibility with industry-standard 3D printing software while maintaining standard web-based 3D visualization.

## ADR-003: Granular Viewport Memoization
**Decision**: Use memoized `NodeRenderer` components with individual store subscriptions.
**Rationale**: React-three-fiber performance degrades linearly with object count if the entire scene graph rerenders. Granular subscriptions isolate updates to modified nodes only.

## ADR-004: State-Driven Bounding Box Caching
**Decision**: Store bounding boxes in the `SceneNode` object and invalidate on transform/param change.
**Rationale**: Assembly logic (Snap, Align) is computation-heavy. Caching bounds avoids repeated DOM/mesh-based calculations during rapid editing.

## ADR-005: Dirty Tracking for Autosave
**Decision**: Implement `isDirty` flag in Zustand and use a debounced 3s save loop.
**Rationale**: Prevents redundant HTTP requests to the SQLite backend while ensuring that no more than 3 seconds of work is lost in case of failure.
