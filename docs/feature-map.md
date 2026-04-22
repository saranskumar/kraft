# Feature Map: Kraft CAD v2

## Phase 6: Unified Export System (Complete)
- **Geometry Engine**: Multi-format mesh merging (STL, OBJ) with parametric script isolation.
- **Coordinate Mapping**: Automatic Y-up (Three.js) to Z-up (OpenSCAD) transformation.
- **Export Modes**: Support for "Full Assembly" and "Parametric Only" modes.
- **Diagnostic Feedback**: X-Export-Warnings header system for backend-to-frontend logs.

## Phase 7: Performance + Stability (Complete)
- **Dirty Tracking**: `isDirty` flag for intelligent, debounced autosaves.
- **Rendering Memoization**: Granular `NodeRenderer` subscriptions to prevent full scene rerenders.
- **Bounding Box Caching**: `cachedBounds` on `SceneNode` for accelerated assembly logic.
- **Performance Telemetry**: Debug panel showing object counts and operation timings.
- **Asset Stability**: Support for 3MF imports and cached mesh geometry.
