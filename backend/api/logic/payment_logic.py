import stripe
from api.config import settings
from api.logic.assignment_logic import AssignmentLogic
from api.logic.chat_logic import ChatLogic
from api.router.models import PaymentRequest
from api.storage.models import User
from fastapi import HTTPException

stripe.api_key = settings.stripe_api_key

class PaymentLogic:

    @staticmethod
    def handle_payment_request(payment_request: PaymentRequest, user: User) -> dict:
        """
        Handles the payment request logic.
        
        Args:
            payment_request (dict): The payment request data.
        
        Returns:
            dict: Response indicating success or failure.
        """

        deposit = payment_request.hourly_rate_cents / 2  # Assuming the deposit is half of the hourly rate

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'sgd',
                        'product_data': {
                            'name': settings.stripe_product_name,  # Product name from settings
                        },
                        'unit_amount': int(deposit),  # Final price in cents
                    },
                    'quantity': 1,
                }],
                payment_intent_data={
                    'metadata': {
                        'user_id': user.id,  # Store user ID in metadata
                        'assignment_request_id': payment_request.assignment_request_id,
                    }
                },
                mode = payment_request.mode,  # 'payment' or 'subscription'
                success_url=f"{payment_request.success_url}?session_id={{CHECKOUT_SESSION_ID}}&tutor_id={payment_request.tutor_id}&chat_id={payment_request.chat_id}",
                cancel_url=payment_request.cancel_url,
            )
            return {"session_id": checkout_session['id'],
                    "url": checkout_session["url"]}
        except stripe.error.StripeError as e:
            # Handle Stripe-specific errors
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    @staticmethod
    def handle_stripe_webhook(payload, sig_header: str) -> dict:
        try:
            # Verify the webhook signature
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.stripe_webhook_secret
            )

            # Handle the payment_intent successful
            print(event['type'])
            print(event.keys())

            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']  # contains a stripe.PaymentIntent

                # Example: extract details
                customer_id = payment_intent.get('customer')
                amount_received = payment_intent['amount_received']
                metadata = payment_intent.get('metadata', {})

                # Change status of assignment request to accepted
                owner_id, requester_id = AssignmentLogic.accept_assignment_request(metadata['assignment_request_id'])
                
                preview = ChatLogic.get_or_create_private_chat(owner_id, requester_id)

                ChatLogic.unlock_chat(preview["id"], owner_id)

                return {"status": "success"}

        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid payload: {e}")
        except stripe.error.SignatureVerificationError as e:
            raise HTTPException(status_code=400, detail=f"Signature verification failed: {e}")

