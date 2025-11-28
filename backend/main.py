from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.payments import router as payments_router

app = FastAPI()
origins = [
    "https://Eunice-ctrlz.github.com",
    "https://github.com/Eunice-ctrlz/FastFibersWebsite",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payments_router)
