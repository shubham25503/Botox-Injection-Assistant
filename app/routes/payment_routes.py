from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schema import UserLogin, UserOut, UserSignup, UserEdit, ResetPassword, UserOut2
from app.utils.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
import stripe
from app.config import STRIPE_SECRET_KEY

router = APIRouter(tags=["Payment"])


stripe.api_key = STRIPE_SECRET_KEY

@router.post("/create-checkout-session",  dependencies=[Depends(get_current_user)])
async def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "My Product",
                        },
                        "unit_amount": 5000,  # $50.00
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="https://yourdomain.com/success",
            cancel_url="https://yourdomain.com/cancel",
        )
        return {"sessionId": session.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))