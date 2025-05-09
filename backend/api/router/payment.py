import stripe
from fastapi import APIRouter, Depends, HTTPException

from backend.api.router.auth import RouterAuthUtils

router = APIRouter()

@router.post("/api/payment/checkout")
def payment():
    """
    Create a checkout session with Stripe.
    """
    try:
        # Create a new checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "T-shirt",
                        },
                        "unit_amount": 2000,
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )
        return {"sessionId": session.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))