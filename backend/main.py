from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import payment
from backend.database import engine, Base
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Payment API",
    description="M-Pesa Payment Processing API",
    version="1.0.0"
)

# CORS Configuration - CRITICAL FOR FRONTEND TO WORK
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://Eunice-ctrlz.github.io",  # Your GitHub Pages site
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5500",
        "*"  # Allow all origins (remove in production for better security)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include payment router
app.include_router(payment.router, tags=["payments"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Payment API is running",
        "version": "1.0.0",
        "endpoints": {
            "payment": "/payment",
            "get_payments": "/payments",
            "get_customers": "/customers",
            "get_services": "/services"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

# Run the application
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)