import stripe
from api.config import settings
from api.logic.assignment_logic import AssignmentLogic
from api.logic.chat_logic import ChatLogic
from api.logic.tutor_logic import TutorLogic
from api.router.models import PaymentRequest
from api.storage.models import User, Tutor, AssignmentRequest
from api.services.email_service import GmailEmailService
from fastapi import HTTPException
from typing import Callable
from sqlalchemy.orm import Session
from api.storage.storage_service import StorageService

stripe.api_key = settings.stripe_api_key

class PaymentLogic:

    @staticmethod
    def handle_payment_request(payment_request: PaymentRequest, assert_user_authorized: Callable[[int], None]) -> dict:
        """
        Handles the payment request logic.
        
        Args:
            payment_request (dict): The payment request data.
        
        Returns:
            dict: Response indicating success or failure.
        """

        try:
            assert_user_authorized(AssignmentLogic.get_assignment_owner_id(payment_request.assignment_request_id)) 

            lesson_duration = AssignmentLogic.get_lesson_duration(
                payment_request.assignment_request_id
            )

            hourly_rate = AssignmentLogic.get_request_hourly_rate(
                payment_request.assignment_request_id
            )

            num_hours = lesson_duration / 60  # Convert minutes to hours
            hourly_rate_cents = hourly_rate * 100  # Convert dollars to cents
            fee = num_hours * hourly_rate_cents  # Total fee in cents
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'sgd',
                        'product_data': {
                            'name': settings.stripe_product_name,  # Product name from settings
                        },
                        'unit_amount': int(fee),  # Final price in cents
                    },
                    'quantity': 1,
                }],
                payment_intent_data={
                    'metadata': {
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
            raise HTTPException(status_code=503, detail=f"Payment processing error on stripe. {e.user_message}")
        except Exception as e:
            raise e
        
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
                metadata = payment_intent.get('metadata', {})

                # Change status of assignment request to accepted
                owner_id, requester_id = AssignmentLogic.accept_assignment_request(int(metadata['assignment_request_id']))
                
                preview = ChatLogic.get_or_create_private_chat(owner_id, requester_id)

                ChatLogic.unlock_chat(preview.id, owner_id)

                # Send email to tutor about successful payment
                with Session(StorageService.engine) as session:
                    # Fetch the tutor's details
                    tutor = session.query(Tutor).filter_by(id=requester_id).first()
                    
                    # Fetch the assignment details
                    assignment_request = session.query(AssignmentRequest).filter_by(id=int(metadata['assignment_request_id'])).first()
                    assignment = assignment_request.assignment

                    if tutor and tutor.user and assignment:
                        # Compose email content
                        email_content = f"""
                        Congratulations! Your assignment request for "{assignment.title}" has been accepted and paid for.

                        Assignment Details:
                        - Title: {assignment.title}
                        - Hourly Rate: ${assignment_request.requested_rate_hourly}
                        - Lesson Duration: {assignment_request.requested_duration} minutes

                        You can now view the details in your dashboard.
                        """
                        print(email_content)
                        # Send email to tutor
                        GmailEmailService.send_email(
                            recipient_email=tutor.user.email,
                            subject=f"Assignment Accepted: {assignment.title}",
                            content=email_content
                        )
                        print(f"Email sent to tutor {tutor.user.email} about assignment acceptance.")

                return {"status": "success"}

        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid payload: {e}")
        except stripe.error.SignatureVerificationError as e:
            raise HTTPException(status_code=400, detail=f"Signature verification failed: {e}")

