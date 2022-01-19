from flask import Flask, request, redirect, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pypaystack import Transaction, Customer, Plan


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(120), nullable=False)
    orders = db.relationship('Orders', backref='customer_name', lazy=True)

    def __repr__(self): # how the object is printed whenever we print it out
        return f"Customers('{self.first_name}','{self.last_name}','{self.email}')"

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    order_status = db.Column(db.String, nullable=False, default='Fulfilled')
    shipping_address = db.Column(db.String(120), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)

    def __repr__(self): # how the object is printed whenever we print it out
        return f"Orders('{self.order_date}','{self.amount}','{self.description}','{self.order_status}','{self.shipping_address}')"

class Vendors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    address = db.Column(db.String(120), unique=True, nullable=False)
    product = db.relationship('Products', backref='vendor_product', lazy=True)
    orders = db.relationship('Orders', backref='vendor_order', lazy=True)

    def __repr__(self): # how the object is printed whenever we print it out
        return f"Vendors('{self.first_name}','{self.last_name}','{self.email}')"

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    price = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String(120), nullable=False)
    variant = db.Column(db.String(120), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)

    def __repr__(self): # how the object is printed whenever we print it out
        return f"Products('{self.name}','{self.price}','{self.brand}','{self.variant}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') 
    product = db.relationship('Products', backref='product_name', lazy=True)

    def __repr__(self): # how the object is printed whenever we print it out
        return f"Category('{self.name}','{self.description}')"


@app.route('/', methods=['POST','GET'])
@app.route('/index', methods=['POST','GET'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

print("Hello World")