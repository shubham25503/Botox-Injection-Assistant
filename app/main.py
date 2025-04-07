from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router
from fastapi.responses import JSONResponse
from app.routes.procedure_routes import router as procedure_router

app = FastAPI(title="Botox-Injection-Predictor")


@app.get("/")
async def root():
    return {"message": "Welcome to the Botox Injection Predictor"}

app.include_router(auth_router, prefix="/auth")
app.include_router(procedure_router, prefix="/procedures")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred on the server.", "details": str(exc)}
    )
