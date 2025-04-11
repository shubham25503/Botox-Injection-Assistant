from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router
from fastapi.responses import JSONResponse
from app.routes.procedure_routes import router as procedure_router
from app.routes.image_data_routes import router as image_router
from app.routes.plan_routes import router as plan_router
from app.routes.stripe_routes import router as stripe_routes
from app.routes.admin_user_routes import router as admin_user_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Botox-Injection-Predictor")

origins = [
    "http://localhost:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Botox Injection Predictor"}

app.include_router(auth_router, prefix="/auth")
app.include_router(procedure_router, prefix="/procedures")
app.include_router(stripe_routes, prefix="/stripe")
app.include_router(admin_user_router, prefix="/admin/users")
app.include_router(image_router, prefix="/image")
app.include_router(plan_router, prefix="/api/plans")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred on the server.", "details": str(exc)}
    )
