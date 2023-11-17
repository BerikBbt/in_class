# from werkzeug.security import generate_password_hash #generates unique password
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin, LoginManager
# from datetime import datetime
# import uuid


# #instantitate all our classes
# db = SQLAlchemy() #makes database object
# login_manager = LoginManager() #makes login manager


# # use login_manager object to create a user_loader function
# @login_manager.user_loader
# def user_loader(user_id):
#     """Given *user_id*, return the associated User object.

#     :param unicode user_id: user_id (email) user to retrieve

#     """
#     return User.query.get(user_id)


# class User(db.Model, UserMixin): 
#     #create table user, all the columns we create
#     user_id = db.Column(db.String, primary_key=True)
#     first_name = db.Column(db.String(30))
#     last_name = db.Column(db.String(30))
#     username = db.Column(db.String(30), nullable=False, unique=True)
#     email = db.Column(db.String(150), nullable=False, unique=True)
#     password = db.Column(db.String, nullable=False)
#     date_added = db.Column(db.DateTime, default=datetime.utcnow)  #this is going to grab a timestamp as soon as a User object is instantiated


#     def __init__(self, username, email, password, first_name="", last_name=""):
#         self.user_id = self.set_id()
#         self.first_name = first_name
#         self.last_name = last_name
#         self.username = username
#         self.email = email 
#         self.password = self.set_password(password) 


#     def set_id(self):
#         return str(uuid.uuid4()) #all this is doing is creating a unique identification token
    
#     def get_id(self):
#         return str(self.user_id) #UserMixin using this method to grab the user_id on the object logged in


#     def __repr__(self):
#         return f"<User: {self.username}>"
    
#     def set_password(self, password):
#         return generate_password_hash(password)



#              DAY3



from werkzeug.security import generate_password_hash #generates unique password
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from datetime import datetime
import uuid
from flask_marshmallow import Marshmallow

#internal imports
from .helpers import get_image


#instantitate all our classes
db = SQLAlchemy() #makes database object
login_manager = LoginManager() #makes login manager
ma = Marshmallow()


# use login_manager object to create a user_loader function
@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)


class User(db.Model, UserMixin): 
    #create table user, all the columns we create
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)  #this is going to grab a timestamp as soon as a User object is instantiated


    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email 
        self.password = self.set_password(password) 


    def set_id(self):
        return str(uuid.uuid4()) #all this is doing is creating a unique identification token
    
    def get_id(self):
        return str(self.user_id) #UserMixin using this method to grab the user_id on the object logged in


    def __repr__(self):
        return f"<User: {self.username}>"
    
    def set_password(self, password):
        return generate_password_hash(password)
    

class Product(db.Model): #db.Model helps translate puthon code
    prod_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String)
    description = db.Column(db.String(200))
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self, name, price, quantity, image="", description=""):
        self.prod_id = self.set_id()
        self.name = name
        self.image = self.set_image(image, name)
        self.description = description
        self.price = price
        self.quantity = quantity 

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_image(self, image, name):

        if not image:
            image = get_image(name)
        return image
    
    def decrement_quantity(self, quantity):

        self.quantity -= int(quantity)
        return self.quantity
    
    def increment_quantity(self, quantity):
        self.quantity += int(quantity)
        return self.quantity
    
    def __repr__(self):
        return f"<Product: {self.name}>"
    

class Customer(db.Model):
    cust_id = db.Column(db.String, primary_key=True)
    date_created = db.Column(db.String, default = datetime.utcnow() )

    prodord = db.relationship('ProdOrder', backref = 'customer', lazy=True)
    def __init__(self, cust_id):
        self.cust_id = cust_id

    def __repr__(self):
        return f"<Customer: {self.cust_id}>"
    


#example of a join table
#because Products can be on many Orders
#and Orders can have many Products (many-to-many) relationship needs a Join table

class ProdOrder(db.Model):
    prodorder_id = db.Column(db.String, primary_key=True)

    prod_id = db.Column(db.String, db.ForeignKey('product.prod_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Numeric(precision = 10, scale = 2), nullable = False)
    order_id = db.Column(db.String, db.ForeignKey('order.order_id'), nullable = False)
    cust_id = db.Column(db.String, db.ForeignKey('customer.cust_id'), nullable = False)


    def __init__(self, prod_id, quantity, price, order_id, cust_id):
        self.prodorder_id = self.set_id()
        self.prod_id = prod_id
        self.quantity = quantity
        self.price = self.set_price(quantity, price)
        self.order_id = order_id
        self.cust_id = cust_id


    def set_id(self):
        return str(uuid.uuid4())
    


    def set_price(self, quantity, price):

        quantity = int(quantity)
        price = float(price)

        self.price = quantity * price
        return self.price
    
    
    def update_quantity(self, quantity):

        self.quantity = int(quantity)
        return self.quantity
    

class Order(db.Model):
    order_id = db.Column(db.String, primary_key=True)
    order_total = db.Column(db.Numeric(precision=10, scale=2), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    prodord = db.relationship('ProdOrder', backref = 'order', lazy=True)


    def __init__(self):
        self.order_id = self.set_id()
        self.order_total = 0.00


    def set_id(self):
        return str(uuid.uuid4())
    
    def increment_ordertotal(self, price):

        self.order_total = float(self.order_total)
        self.order_total += float(price)

        return self.order_total
    
    def decrement_ordertotal(self, price):

        self.order_total = float(self.order_total)
        self.order_total -= float(price)

        return self.order_total
    
    def __repr__(self):
        return f"<Order: {self.order_id}>"



# Create schema class

class ProductSchema(ma.Schema):

    class Meta:
        fields = ['prod_id', 'name', 'description', 'price', 'image', 'quantity']


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
