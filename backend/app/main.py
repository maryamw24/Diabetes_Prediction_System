from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import predict, auth, admin
from app.db import init_db
from fastapi.responses import RedirectResponse


app = FastAPI(title="Diabetes Prediction API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()
@app.get("/")
def root():
    return RedirectResponse(url="/home")

@app.get("/home")
def home():
    return {"message": "Welcome to the Home page"}

# Include routers
app.include_router(predict.router)
app.include_router(auth.router)
app.include_router(admin.router)
