import stripe
from app.config import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY

def fetch_products():
    try:
        prices = stripe.Price.list(
            limit=3,
            expand=["data.product"]
        )

        product_list = []
        for price in prices["data"]:
            product = price["product"]
            product_list.append({
                "product_name": product["name"],
                "description": product["description"],
                "price_id": price["id"],
                "amount": price["unit_amount"] / 100,
                "currency": price["currency"],
                "interval": price.get("recurring", {}).get("interval")
            })

        return product_list
    
    except stripe.error.StripeError as e:
        return {"error": f"Stripe API error: {e.user_message if hasattr(e, 'user_message') else str(e)}"}

    except Exception as e:
        return {"error": "An unexpected error occurred while fetching products."}




def create_checkout_session(data: dict):
    try:
        price_id = data.get("price_id")
        quantity = data.get("quantity")
        success_url = data.get("success_url")
        cancel_url = data.get("cancel_url")

        if not all([price_id, quantity, success_url, cancel_url]):
            raise ValueError("Missing required data fields for checkout session.")

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price": price_id,
                "quantity": quantity
            }],
            success_url=success_url,
            cancel_url=cancel_url
        )
        return {"checkout_url": session.url}

    except stripe.error.CardError as e:
        return {"error": f"Card error: {e.user_message}"}

    except stripe.error.RateLimitError:
        return {"error": "Rate limit exceeded. Please try again later."}

    except stripe.error.InvalidRequestError as e:
        return {"error": f"Invalid request: {e.user_message if hasattr(e, 'user_message') else str(e)}"}

    except stripe.error.AuthenticationError:
        return {"error": "Authentication failed with Stripe."}

    except stripe.error.APIConnectionError:
        return {"error": "Network communication error with Stripe."}

    except stripe.error.StripeError as e:
        return {"error": f"An error occurred: {e.user_message if hasattr(e, 'user_message') else str(e)}"}

    except ValueError as e:
        return {"error": str(e)}

    except Exception as e:
        return {"error": "An unexpected error occurred while creating the checkout session."}