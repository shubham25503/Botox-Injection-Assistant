from pydantic import BaseModel, EmailStr

class CheckoutRequest(BaseModel):
    price_id: str
    quantity: int
    success_url:str
    email: EmailStr
    cancel_url: str

class AfterPayment(BaseModel):
    is_payment_success:bool
    email: EmailStr