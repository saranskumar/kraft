# Kraft CAD v2

A professional, AI-assisted CAD editor for multi-part robotics assemblies. Built with Next.js, FastAPI, and OpenSCAD.

## Features

- **Professional Workspace**: Resizable, multi-panel layout inspired by VS Code.
- **Parametric Templates**: Reusable robotics components (Chassis, Motor Mounts, Battery Trays).
- **AI Design Assistant**: Natural language command generation for assembly manipulation.
- **Real-time Viewport**: High-performance 3D rendering with transform gizmos.
- **OpenSCAD Integration**: Precise geometric kernel for industrial-grade export.
- **Import/Export**: Support for STL/OBJ import and STL assembly export.

## Documentation
Comprehensive technical documentation is available in the [**docs/**](./docs/full.md) folder:
- [Architecture Decisions](./docs/decisions.md)
- [API Contracts](./docs/api-contracts.md)
- [Workflow Logic](./docs/workflow-logic.md)
- [Feature Map](./docs/feature-map.md)

## Tech Stack

- **Frontend**: Next.js 14, Tailwind CSS, Lucide Icons, Zustand, Three.js / React Three Fiber.
- **Backend**: FastAPI, Python 3.10+, OpenSCAD, Google Gemini 3.
- **DevOps**: Project memory persistence via `.agent` and `.project`.

## Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/) (pnpm recommended)
- [Python 3.10+](https://www.python.org/)
- [OpenSCAD](https://openscad.org/) installed and path set in `.env`

### Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd kraft
   ```

2. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   # Create .env with OPENSCAD_PATH and GEMINI_API_KEY
   uvicorn main:app --reload
   ```

3. **Setup Frontend**
   ```bash
   cd frontend
   pnpm install
   pnpm dev
   ```

## Workflow
- **Shortcuts**: `Delete` to remove, `Ctrl+D` to duplicate, `Ctrl+Z` to undo, `F` to focus.
- **AI Assistant**: Use the right sidebar to request changes like "Add a motor mount" or "Make the chassis wider".

## License
MIT
