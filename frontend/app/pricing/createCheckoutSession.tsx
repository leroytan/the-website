export async function createCheckoutSession(data: {
    mode: 'payment' | 'subscription';
  price_id: string;
  success_url: string;
  cancel_url: string;
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