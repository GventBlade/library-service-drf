import stripe
from django.conf import settings
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_session(borrowing, money_to_pay, request):
    success_url = request.build_absolute_uri(reverse('payments:payment-success'))
    cancel_url = request.build_absolute_uri(reverse('payments:payment-cancel'))

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": int(money_to_pay * 100),
                "product_data": {
                    "name": f"Borrowing: {borrowing.book.title}",
                    "description": f"From {borrowing.borrow_date} to {borrowing.expected_return_date}",
                },
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url,
    )
    return session.url, session.id
