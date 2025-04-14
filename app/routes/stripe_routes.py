from fastapi import APIRouter, HTTPException
from app.services.stripe_service import fetch_products, create_checkout_session, get_payment_details
from app.schemas.stripe_schema import CheckoutRequest, AfterPayment
from app.utils.functions import create_response, handle_exception
router = APIRouter(tags=["stripe"])


@router.get("/stripe/products")
def get_products():
    return create_response(200,True,"Products Fetched Successfully",fetch_products())

@router.put("/stripe/after-payment")
async def after_payment(request: AfterPayment):
    try:
        data = request.dict()
        await get_payment_details(data)
        return create_response(200,True,"",None)
    except Exception as e:
        print("stripe post checkout", e)
        raise HTTPException(status_code=400,detail=handle_exception(e,""))


@router.post("/stripe/checkout")
async def checkout(request:CheckoutRequest):
    try:
        data = request.dict()
        url = await create_checkout_session(data)
        return create_response(200,True,"",{"checkout_url": url})
    except Exception as e:
        print("stripe post checkout", e)
        raise HTTPException(status_code=400, detail=handle_exception(e,""))
