# Architectural Decisions

## ADR 001: Multi-Panel Workspace Layout
- **Context**: The editor needed to transition from a prototype to a professional CAD tool.
- **Decision**: Adopted a VS Code-inspired layout with resizable sidebars and a bottom panel.
- **Consequences**: Improved workspace utility, allowed for parallel viewing of properties and chat history.

## ADR 002: Local Workspace Memory (Rule 98)
- **Context**: Project context was previously stored in system app data, making it hard to share or persist with the repo.
- **Decision**: Migrated all artifacts to `.agent/` and `.project/` folders within the root.
- **Consequences**: Enhanced context persistence and repository portability.

## ADR 003: Gemini 3 AI Integration
- **Context**: Needed a powerful, structured command generator.
- **Decision**: Switched to `gemini-3-flash-preview` for low latency and high instruction adherence.
- **Consequences**: Reliable generation of complex JSON command arrays.

## ADR 004: Parametric Geometry with OpenSCAD
- **Context**: Required industrial-grade STL output.
- **Decision**: Used OpenSCAD as the geometric kernel, mapping Three.js coordinates (Y-up) to OpenSCAD coordinates (Z-up).
- **Consequences**: High-fidelity 3D printable output for robotic parts.
