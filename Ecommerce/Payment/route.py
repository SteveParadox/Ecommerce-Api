from flask import *
from Ecommerce.Users.decorator import token_required
from Ecommerce.model import Order

payment = Blueprint('payment', __name__)



@payment.route('/api/payment/crypto', methods=['POST'])
def crypto_payment():
    # Get payment details from the request
    amount = request.json.get('amount')
    currency = request.json.get('currency')
    address = request.json.get('address')
    order_id = request.json.get('order_id')

    # Send payment request to the crypto payment gateway
    payload = {
        'amount': amount,
        'currency': currency,
        'address': address,
        'order_id': order_id
    }
    response = requests.post('https://crypto-payment-gateway.com/api/pay', json=payload)

    # Handle payment response
    if response.status_code == 200:
        # Payment successful
        return jsonify({'message': 'Payment successful!'})
    else:
        # Payment failed
        error_message = response.json().get('error')
        return jsonify({'message': f'Payment failed: {error_message}'}), 400



@payment.route('/payments', methods=['GET'])
@token_required
def get_payments(current_user):
    # Get all payments associated with the current user
    payments = Payment.query.filter_by(user_id=current_user.id).all()
    payments_json = []
    for payment in payments:
        payment_json = {
            'id': payment.id,
            'payment_date': payment.payment_date,
            'amount': payment.amount,
            'order_id': payment.order_id
        }
        payments_json.append(payment_json)

    return jsonify({'payments': payments_json})

@payment.route('/api/checkout', methods=['POST'])
@token_required
def checkout(current_user):
    user_orders = Order.query.filter_by(user_id=current_user.id).all()
    order_ids = [order.id for order in user_orders]
    if not order_ids:
        return jsonify({'error': 'No orders found for the user'}), 400
    
    orders = Order.query.filter(Order.id.in_(order_ids)).all()
    if len(orders) != len(order_ids):
        return jsonify({'error': 'One or more orders not found'}), 404
    
    total_price = sum([order.total_price for order in orders])
    if total_price <= 0:
        return jsonify({'error': 'Total price must be greater than zero'}), 400
    print(total_price)
    
    # You can add your payment processing logic here
    # For example, you can use a third-party payment API like Stripe
    # or a payment gateway provided by your bank.
    # You will need to replace the placeholders below with your own code.
    
    try:
        charge = stripe.Charge.create(
            amount=total_price * 100, # Stripe accepts amounts in cents
            currency='usd',
            description='Example charge',
            source=data.get('stripe_token')
        )
        
        # If the payment was successful, update the orders with a status of "paid"
        for order in orders:
            order.status = 'paid'
        db.session.commit()
        
        return jsonify({'message': 'Payment successful', 'charge_id': charge.id}), 200
    
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        return jsonify({'error': e.user_message}), 400
    
    except stripe.error.StripeError as e:
        # Something else happened, completely unrelated to Stripe
        return jsonify({'error': 'Payment failed'}), 500



