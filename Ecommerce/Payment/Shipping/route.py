from flask import *
from Ecommerce.Users.decorator import token_required
from Ecommerce.model import *

shipping = Blueprint('shipping', __name__)

# Shipping Address endpoints
@shipping.route('/shipping_addresses/<int:order_id>', methods=['POST'])
@token_required
def add_shipping_address(current_user, order_id):
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    city = data.get('city')
    state = data.get('state')
    country = data.get('country')
    zip_code = data.get('zip_code')
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first()
    print(order.status)
    if order.status != "shipped" and order.status != "delivered":
            # Create the shipping address object
            shipping_address = ShippingAddress(
                order_id=order_id, 
                name=name, 
                address=address, 
                city=city, 
                state=state, 
                country=country, 
                zip_code=zip_code,
            )
            db.session.add(shipping_address)
            order.status = "shipped"
            db.session.commit()
    else:
        return jsonify({'error': 'Order not found'}), 404

    # Convert shipping address to JSON format
    shipping_address_json = {
        'id': shipping_address.id,
        'order_id': shipping_address.order_id,
        'name': shipping_address.name,
        'address': shipping_address.address,
        'city': shipping_address.city,
        'state': shipping_address.state,
        'country': shipping_address.country,
        'zip_code': shipping_address.zip_code
    }

    return jsonify({'shipping_address': shipping_address_json}), 201




@shipping.route('/orders/<int:order_id>/shipping', methods=['GET'])
@token_required
def get_shipping_address(current_user,order_id):

    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    shipping_address = ShippingAddress.query.filter_by(order_id=order_id).first()
    if not shipping_address:
        return jsonify({'error': 'Shipping address not found'}), 404
    _schema = ShippingAddressSchema()
    result = _schema.dump(shipping_address)
    return jsonify(result)

@shipping.route('/orders/<int:order_id>/shipping/update', methods=['PUT'])
@token_required
def update_shipping_address(current_user,order_id):
    # Get the order
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404
   
    shipping_address = ShippingAddress.query.filter_by(order_id=order_id).first()
    if not shipping_address:
        return jsonify({'error': 'Shipping address not found'}), 404
    data = request.get_json()
    shipping_address.name = data.get('name', shipping_address.name)
    shipping_address.address = data.get('address', shipping_address.address)
    shipping_address.city = data.get('city', shipping_address.city)
    shipping_address.state = data.get('state', shipping_address.state)
    shipping_address.country = data.get('country', shipping_address.country)
    shipping_address.zip_code = data.get('zip_code', shipping_address.zip_code)

    # Update the shipping address in the database
    db.session.commit()

    return jsonify({'message': 'Shipping address updated successfully'})

@shipping.route('/orders/<int:order_id>/shipping/delete', methods=['DELETE'])
@token_required
def delete_shipping_address(current_user,order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    shipping_address = ShippingAddress.query.filter_by(order_id=order_id).first()
    if not shipping_address:
        return jsonify({'error': 'Shipping address not found'}), 404
    db.session.delete(shipping_address)
    order.status = "placed"
    db.session.commit()

    return jsonify({'message': 'Shipping address updated deleted'})


@shipping.route('/api/orders/<int:order_id>/delivery', methods=['PUT'])
@token_required
def update_delivery_status(current_user, order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    data = request.get_json()
    if not data or 'delivery_status' not in data:
        return jsonify({'error': 'Missing or invalid required fields'}), 400
    
    delivery_status = data['delivery_status']
    if delivery_status not in ['shipped', 'delivered']:
        return jsonify({'error': 'Invalid delivery status'}), 400
    
    order.delivery_status = delivery_status
    db.session.commit()
    
    return jsonify({'message': f'Delivery status for order {order_id} updated successfully'}), 200
