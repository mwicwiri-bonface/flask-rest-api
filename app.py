import os
from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecret'

# init db
db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.route('/products/', methods=['POST'])
def add_product():
    """ Add a new product """
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


@app.route('/products/', methods=['GET'])
def get_products():
    """ Get all products """
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return products_schema.jsonify(result)


@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    """ Get a single product """
    product = Product.query.get(id)
    return product_schema.jsonify(product)


@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    """ Update a product """
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()

    return product_schema.jsonify(product)


# runserver
if __name__ == '__main__':
    app.run(debug=True)
