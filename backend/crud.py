from sqlalchemy.orm import Session
from .models import Customer, Service, Payment

def create_customer(db: Session, name: str, phone: str):
    customer = Customer(name=name, phone=phone)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def get_service(db: Session, service_id: int):
    return db.query(Service).filter(Service.id == service_id).first()

def create_payment(db: Session, customer_id: int, service_id: int, amount: float, checkout_request_id: str = None):
    payment = Payment(
        customer_id=customer_id, 
        service_id=service_id, 
        amount=amount,
        checkout_request_id=checkout_request_id,
        status="Pending"
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

def update_payment_status_by_checkout_id(db: Session, checkout_request_id: str, status: str):
    payment = db.query(Payment).filter(Payment.checkout_request_id == checkout_request_id).first()
    if payment:
        payment.status = status
        db.commit()
        db.refresh(payment)
    return payment

def get_payment(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()

def get_customer_by_phone(db: Session, phone: str):
    return db.query(Customer).filter(Customer.phone == phone).first()