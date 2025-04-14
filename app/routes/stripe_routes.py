from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.stripe_service import fetch_products, create_checkout_session, get_payment_details
from app.schemas.stripe_schema import CheckoutRequest, AfterPayment

router = APIRouter(tags=["stripe"])


@router.get("/stripe/products")
def get_products():
    return {"products": fetch_products()}

@router.put("/stripe/after-payment")
async def after_payment(request: AfterPayment):
    try:
        data = request.dict()
        await get_payment_details(data)
    except Exception as e:
        print("stripe post checkout", e)
        return JSONResponse(status_code=400, content={"error": str(e)})


@router.post("/stripe/checkout")
async def checkout(request:CheckoutRequest):
    try:
        data = request.dict()
        url = await create_checkout_session(data)
        return {"checkout_url": url}
    except Exception as e:
        print("stripe post checkout", e)
        return JSONResponse(status_code=400, content={"error": str(e)})
