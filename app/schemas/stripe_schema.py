from pydantic import BaseModel

class CheckoutRequest(BaseModel):
    price_id: str
    quantity: int
    success_url:str
    cancel_url: str
    