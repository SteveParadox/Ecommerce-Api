from flask import *

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