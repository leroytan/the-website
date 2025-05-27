from api.logic.payment_logic import PaymentLogic
from api.router.auth_utils import RouterAuthUtils
from api.router.models import PaymentRequest
from api.storage.models import User
from fastapi import APIRouter, Depends, Request

router = APIRouter()

@router.post("/api/payment/create-checkout-session")    
async def create_checkout_session(payment_request: PaymentRequest, user: User = Depends(RouterAuthUtils.get_current_user)):
    return PaymentLogic.handle_payment_request(payment_request, user)

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('Stripe-Signature')

    return PaymentLogic.handle_stripe_webhook(payload, sig_header)
    