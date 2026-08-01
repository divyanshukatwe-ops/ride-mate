from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

from routes import router as rides_router
import data

app = FastAPI(
    title="RideMate API",
    description="Backend API for RideMate – College Auto & Cab Pooling Hackathon Prototype",
    version="1.0.0"
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(rides_router, prefix="/api")

# Static directory path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

@app.on_event("startup")
def startup_event():
    """Ensure 10 sample rides are pre-loaded on application start."""
    data.seed_sample_data()

@app.get("/")
def read_root():
    """Serve the interactive web app UI directly from Python FastAPI server."""
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "app": "RideMate – College Auto & Cab Pooling API",
        "status": "Online",
        "documentation": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8050, reload=True)
