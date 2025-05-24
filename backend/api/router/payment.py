import stripe
from api.config import settings
from api.router.auth_utils import RouterAuthUtils
from api.storage.models import User
from fastapi import APIRouter, Depends, HTTPException, Request

stripe.api_key = settings.stripe_api_key

router = APIRouter()

@router.post("/api/payment/create-checkout-session")    
async def create_checkout_session(request: Request, user: User = Depends(RouterAuthUtils.get_current_user)):
    data = await request.json()
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price': data['price_id'],  # Price ID from the Stripe dashboard
                'quantity': 1,
            }],
            mode = data['mode'],
            success_url=f"{data['success_url']}?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=data['cancel_url'],
            metadata={
                'app_email': user.email,  # Custom metadata to link Stripe data to your user
            }
        )
        return {"session_id": checkout_session['id'],
                "url": checkout_session["url"]}
    except stripe.error.StripeError as e:
        # Handle Stripe-specific errors
        raise HTTPException(status_code=400, detail=str(e.user_message))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
