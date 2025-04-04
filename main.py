from fastapi import FastAPI
from fastapi.responses import JSONResponse
from face_detection1 import face_detection_router

app = FastAPI(title="Botox-Injection-Predictor")

# Include the video feed route
app.include_router(face_detection_router, tags=["face_detection"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Botox Injection Predictor"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred on the server.", "details": str(exc)}
    )
