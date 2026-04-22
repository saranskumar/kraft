from fastapi import APIRouter

router = APIRouter()

@router.post("/geometry/preview")
def preview_geometry():
    # Placeholder for Phase 2+
    return {"status": "not_implemented"}
