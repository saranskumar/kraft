from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes import health, geometry, export, ai, projects
from fastapi.staticfiles import StaticFiles
import os

load_dotenv(override=True)

app = FastAPI(title="Kraft CAD v2 API")

# Ensure uploads directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

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
app.include_router(projects.router)
