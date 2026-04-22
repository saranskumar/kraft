from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes import health, geometry, export, ai

load_dotenv(override=True)

app = FastAPI(title="Kraft CAD v2 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(geometry.router)
app.include_router(export.router)
app.include_router(ai.router)
