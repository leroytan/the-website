from fastapi import APIRouter, Depends, Request

from api.logic.auth_logic import AuthLogic
from api.logic.payment_logic import PaymentLogic
from api.router.auth_utils import RouterAuthUtils
from api.router.models import PaymentRequest
from api.storage.models import User

router = APIRouter()


@router.post("/api/payment/create-checkout-session")
async def create_checkout_session(
    payment_request: PaymentRequest,
    user: User = Depends(RouterAuthUtils.get_current_user),
) -> dict[str, str]:
    assert_user_authorized = AuthLogic.create_assert_user_authorized(user.id)

    return PaymentLogic.handle_payment_request(payment_request, assert_user_authorized)


@router.post("/webhook/stripe")
async def stripe_webhook(request: Request) -> dict:
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")

    print("Received Stripe webhook")

    return PaymentLogic.handle_stripe_webhook(payload, sig_header)
