from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

# Import backend FastAPI app
from backend.main import app as backend_app

app = FastAPI()

# Mount backend routes under /api
app.mount("/api", backend_app)

# Serve static frontend (assumes `frontend/dist` is the build output)
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
