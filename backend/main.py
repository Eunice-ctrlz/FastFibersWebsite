from .config import settings
from .database import engine, Base

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.payments import router as payments_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payments_router)
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    print("Database tables ensured.") 
