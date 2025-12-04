from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..database import SessionLocal, engine, Base, get_db
from ..models import Customer, Service, Payment
from ..mpesa import stk_push
from ..crud import (
    create_customer,
    get_customer_by_phone,
    get_service,
    create_payment,
    update_payment_status_by_checkout_id,
    get_payment
)


router = APIRouter()


class PaymentRequest(BaseModel):
    phone: str
    amount: float
    service_id: Optional[int] = None


@router.post("/payment")
async def make_payment(payment: PaymentRequest, db: Session = Depends(get_db)):
    """
    Process M-Pesa payment and save to database
    """
    print("=" * 50)
    print("PAYMENT REQUEST RECEIVED!")
    print(f"Phone: {payment.phone}")
    print(f"Amount: {payment.amount}")
    print(f"Service ID: {payment.service_id}")
    print("=" * 50)
    
    try:
        # Initiate M-Pesa STK push
        mpesa_response = stk_push(payment.phone, payment.amount)
        print("M-Pesa Response:", mpesa_response)
        
        response_code = mpesa_response.get('ResponseCode')
        checkout_request_id = mpesa_response.get('CheckoutRequestID', '')
        
        if response_code == '0':
            print("✓ M-Pesa request successful")
            
            # Get or create customer
            customer = get_customer_by_phone(db, payment.phone)
            
            if not customer:
                customer = create_customer(db, name="Customer", phone=payment.phone)
                print(f"✓ New customer created with ID: {customer.id}")
            else:
                print(f"✓ Existing customer found with ID: {customer.id}")
            
            # Get service if provided
            service = None
            if payment.service_id:
                service = get_service(db, payment.service_id)
                if not service:
                    print(f"⚠ Service ID {payment.service_id} not found, proceeding without service")
            
            # Save payment to database
            db_payment = create_payment(
                db=db,
                customer_id=customer.id,
                service_id=payment.service_id if service else None,
                amount=payment.amount,
                checkout_request_id=checkout_request_id
            )
            
            print(f"✓ Payment saved to database with ID: {db_payment.id}")
            print(f"✓ Checkout Request ID: {checkout_request_id}")
            print(f"✓ Status: {db_payment.status}")
            print("=" * 50)
            
            return {
                "status": "success",
                "message": "STK push sent successfully! Check your phone.",
                "payment_id": db_payment.id,
                "customer_id": customer.id,
                "checkout_request_id": checkout_request_id,
                "payment_status": db_payment.status,
                "mpesa_response": mpesa_response
            }
        else:
            # M-Pesa request failed
            error_message = mpesa_response.get('errorMessage', 'Unknown error')
            print(f"✗ M-Pesa request failed: {error_message}")
            print("=" * 50)
            
            return {
                "status": "error",
                "message": f"M-Pesa request failed: {error_message}",
                "mpesa_response": mpesa_response
            }
            
    except Exception as e:
        print(f"✗ Exception occurred: {str(e)}")
        print("=" * 50)
        db.rollback()
        
        return {
            "status": "error",
            "message": f"Payment processing failed: {str(e)}"
        }


@router.get("/payments")
async def get_all_payments(db: Session = Depends(get_db)):
    """
    Get all payments from database
    """
    try:
        payments = db.query(Payment).all()
        return {
            "status": "success",
            "count": len(payments),
            "payments": [
                {
                    "id": p.id,
                    "customer_id": p.customer_id,
                    "service_id": p.service_id,
                    "amount": p.amount,
                    "status": p.status,
                    "checkout_request_id": p.checkout_request_id,
                    "created_at": str(p.created_at) if p.created_at else None
                }
                for p in payments
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@router.get("/payments/{payment_id}")
async def get_payment_by_id(payment_id: int, db: Session = Depends(get_db)):
    """
    Get a specific payment by ID
    """
    try:
        payment = get_payment(db, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        return {
            "status": "success",
            "payment": {
                "id": payment.id,
                "customer_id": payment.customer_id,
                "service_id": payment.service_id,
                "amount": float(payment.amount),
                "status": payment.status,
                "checkout_request_id": payment.checkout_request_id,
                "created_at": str(payment.created_at) if payment.created_at else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@router.get("/customers")
async def get_all_customers(db: Session = Depends(get_db)):
    """
    Get all customers from database
    """
    try:
        customers = db.query(Customer).all()
        return {
            "status": "success",
            "count": len(customers),
            "customers": [
                {
                    "id": c.id,
                    "name": c.name,
                    "phone": c.phone
                }
                for c in customers
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@router.get("/services")
async def get_all_services(db: Session = Depends(get_db)):
    """
    Get all services from database
    """
    try:
        services = db.query(Service).all()
        return {
            "status": "success",
            "count": len(services),
            "services": [
                {
                    "id": s.id,
                    "name": s.name,
                    "amount": float(s.amount)
                }
                for s in services
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }