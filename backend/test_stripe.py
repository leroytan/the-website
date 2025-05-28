import os

import stripe
from dotenv import load_dotenv

load_dotenv(".env") # or load_dotenv("config/.env") if it's in a subdirectory

# Set your secret key (don't hardcode this in production)
stripe.api_key = os.getenv("STRIPE_API_KEY")

base_price = 5000  # $50 in cents
experience_multiplier = 1.2
session_duration_multiplier = 1.5

dynamic_price = base_price * experience_multiplier * session_duration_multiplier

# Step 3: Create a checkout session with the dynamically calculated price
checkout_session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': "TutorMatch Fee",
            },
            'unit_amount': int(dynamic_price),  # Final price in cents
        },
        'quantity': 1,
    }],
    mode='payment',
    success_url='https://your-site.com/success',
    cancel_url='https://your-site.com/cancel',
)

print(f"Checkout session created: {checkout_session.id}")
