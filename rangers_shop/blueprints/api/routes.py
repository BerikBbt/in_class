import dataclasses
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from rangers_shop.models import Customer, Product, ProdOrder, Order, db, product_schema, products_schema



api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/token', methods = ['GET', 'POST'])
def token():

    data = request.json
    if data:
        client_id = data['client_id']
        access_token = create_access_token(identity=client_id)
        return {
            'status': 200,
            'access_token': access_token
        }
    else:
        return {
            'status' : 400,
            'message' : 'Missing Client Id. Try Again.'
        }
    

@api.route('/shop')
@jwt_required()
def get_shop():

    allprods = Product.query.all()

    response = products_schema.dump(allprods)
    return jsonify(response)

@api.route('/order/<cust_id>', methods = ['POST'])
@jwt_required()
def create_order(cust_id):
    
    data = request.json

    customer_order = data['order']

    customer = Customer.query.filter(Customer.cust_id == cust_id).first()
    if not customer:
        customer = Customer(cust_id)
        db.session.add(customer)

    order = Order()
    db.session.add(order)

    for product in customer_order:

        prodorder = ProdOrder(product['prod_id'], product['quantity'], product['price'], order.order_id, customer.cust_id )
        db.session.add(prodorder)

        order.increment_ordertotal(prodorder.price)

        current_product = Product.query.get(product['prod_id'])
        current_product.decrement_quantity(product['quantity'])


    db.session.commit()

    return {
        'status' : 200,
        'message' : 'New Order was created.'
    }

@api.route('/order/<cust_id>')
@jwt_required()
def get_orders(cust_id):


    prodorder = ProdOrder.query.filter(ProdOrder.cust_id == cust_id).all()


    data = []

    for order in prodorder:

        product = Product.query.filter(Product.prod_id == order.prod_id).first()

        product_dict = product_schema.dump(product)

        product_dict['quantity'] = order.quantity
        product_dict['order_id'] = order.order_id
        product_dict['id'] = order.prodorder_id

        data.append(product_dict)

    return jsonify(data)

@api.route('/order/update/<order_id>', methods = ['PUT'])
@jwt_required()
def update_order(order_id):

    data = request.json
    new_quantity = int(data['quantity'])
    prod_id = data['prod_id']


    prodorder = ProdOrder.query.filter(ProdOrder.order_id == order_id, ProdOrder.prod_id == prod_id).first()
    order = Order.query.get(order_id)
    product = Product.query.get(prod_id)

    prodorder.set_price(product.price, new_quantity)

    diff = abs(new_quantity - prodorder.quantity)

    if prodorder.quantity > new_quantity:
        product.increment_quantity(diff)
        order.decrement_ordertotal(prodorder.price)

    elif prodorder.quantity < new_quantity:
        product.decrement_quantity(diff)
        order.increment_ordertotal(prodorder.price)

    prodorder.update_quantity(new_quantity)

    db.session.commit()

    return {
        'status': 200,
        'message': 'Order was Updated Successfully'
    }

@api.route('/order/delete/<order_id>', methods = ['DELETE'])
@jwt_required()
def delete_order(order_id):

    data = request.json
    prod_id = data['prod_id']


    prodorder = ProdOrder.query.filter(ProdOrder.order_id == order_id, ProdOrder.prod_id == prod_id).first()
    order = Order.query.get(order_id)
    product = Product.query.get(prod_id)


    order.decrement_ordertotal(prodorder.price) #less $ because deleted a product from our order
    product.increment_quantity(prodorder.quantity) #getting back some total quantity available to sell 

    db.session.delete(prodorder)
    db.session.commit()

    return {
        'status' : 200,
        'message': 'Order was Deleted Successfully'
    }