from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import os

# Direct imports from backend (NO routers)
from backend.database import SessionLocal, Base, engine
from backend.models import Customer, Service, Payment
from backend.mpesa import stk_push
from backend.crud import (
    create_customer,
    get_customer_by_phone,
    get_service,
    create_payment,
    get_payment
)

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
except Exception as e:
    print(f"✗ Database error: {e}")

# Initialize FastAPI
app = FastAPI(
    title="Payment API",
    description="M-Pesa Payment Processing API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://eunice-ctrlz.github.io", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Models
class PaymentRequest(BaseModel):
    phone: str
    amount: float
    service_id: Optional[int] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ENDPOINTS
@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Payment API is running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/payment")
async def make_payment(payment: PaymentRequest, db: Session = Depends(get_db)):
    print("=" * 50)
    print(f"PAYMENT: {payment.phone} - {payment.amount}")
    print("=" * 50)
    
    try:
        mpesa_response = stk_push(payment.phone, payment.amount)
        response_code = mpesa_response.get('ResponseCode')
        checkout_request_id = mpesa_response.get('CheckoutRequestID', '')
        
        if response_code == '0':
            customer = get_customer_by_phone(db, payment.phone)
            if not customer:
                customer = create_customer(db, name="Customer", phone=payment.phone)
            
            service = None
            if payment.service_id:
                service = get_service(db, payment.service_id)
            
            db_payment = create_payment(
                db=db,
                customer_id=customer.id,
                service_id=payment.service_id if service else None,
                amount=payment.amount,
                checkout_request_id=checkout_request_id
            )
            
            print(f"✓ Payment saved: {db_payment.id}")
            
            return {
                "status": "success",
                "message": "STK push sent successfully! Check your phone.",
                "payment_id": db_payment.id,
                "checkout_request_id": checkout_request_id
            }
        else:
            return {
                "status": "error",
                "message": f"M-Pesa failed: {mpesa_response.get('errorMessage')}"
            }
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        return {"status": "error", "message": str(e)}

@app.get("/payments")
async def get_all_payments(db: Session = Depends(get_db)):
    try:
        payments = db.query(Payment).all()
        return {
            "status": "success",
            "count": len(payments),
            "payments": [{
                "id": p.id,
                "amount": float(p.amount),
                "status": p.status,
                "checkout_request_id": p.checkout_request_id
            } for p in payments]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/customers")
async def get_all_customers(db: Session = Depends(get_db)):
    try:
        customers = db.query(Customer).all()
        return {
            "status": "success",
            "customers": [{"id": c.id, "name": c.name, "phone": c.phone} for c in customers]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/services")
async def get_all_services(db: Session = Depends(get_db)):
    try:
        services = db.query(Service).all()
        return {
            "status": "success",
            "services": [{"id": s.id, "name": s.name, "amount": float(s.amount)} for s in services]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.on_event("startup")
async def startup():
    print("=" * 50)
    print("🚀 APPLICATION STARTED")
    print("=" * 50)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)