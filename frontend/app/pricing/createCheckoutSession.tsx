export async function createCheckoutSession(data: {
    mode: 'payment' | 'subscription';
    success_url: string;
    cancel_url: string;
    hourly_rate_cents: number;
    assignment_request_id: number;
    tutor_id: number;
    chat_id?: number;
}) {
  const response = await fetch('/api/payment/create-checkout-session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Failed to create checkout session');
  }

  return response.json();
}