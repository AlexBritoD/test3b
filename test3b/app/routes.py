from flask import Blueprint, request, jsonify
from .models import db, Product, Order

main = Blueprint('main', __name__)


@main.route('/api/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    products_list = []
    for product in products:
        products_list.append({
            'id': product.id,
            'sku': product.sku,
            'name': product.name,
            'stock': product.stock
        })
    return jsonify(products_list), 200

@main.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    if 'sku' not in data or 'name' not in data:
        return jsonify({'message': 'SKU and name are required'}), 400
    
    existing_product = Product.query.filter_by(sku=data['sku']).first()
    if existing_product:
        return jsonify({'message': 'Product with this SKU already exists'}), 400
    
    new_product = Product(sku=data['sku'], name=data['name'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created', 'product_id': new_product.id}), 201

@main.route('/api/inventories/product/<int:product_id>', methods=['PATCH'])
def update_stock(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json
    if 'stock' not in data or not isinstance(data['stock'], int):
        return jsonify({'message': 'Invalid stock value'}), 400
    
    new_stock = product.stock + data['stock']
    if new_stock < 0:
        return jsonify({'message': 'Stock cannot be negative'}), 400
    
    product.stock = new_stock
    db.session.commit()
    return jsonify({'message': 'Stock updated', 'new_stock': product.stock}), 200

@main.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    product = Product.query.get_or_404(data['product_id'])
    if product.stock < data['quantity']:
        return jsonify({'message': 'Not enough stock'}), 400
    product.stock -= data['quantity']
    new_order = Order(product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created', 'order_id': new_order.id}), 201

@main.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'sku': product.sku,
        'name': product.name,
        'stock': product.stock
    }), 200

@main.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return '', 204

@main.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({
        'id': order.id,
        'product_id': order.product_id,
        'quantity': order.quantity
    }), 200

@main.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return '', 204