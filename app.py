from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


#Instantiating the App
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Initializing sqlalchemy
db = SQLAlchemy(app)

#Initializing marshamaloow
ma = Marshmallow(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer,primary_key=True)
    name =db.Column(db.String(100),unique=True,nullable=False)
    description =db.Column(db.String(200),unique=True,nullable=False)
    price =db.Column(db.Float,nullable=False)
    qty = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        
        return f"{self.name} ,{self.description} ,{self.price} ,{self.qty}"


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','price','qty')

#initialize schema 
product_schema = ProductSchema(many=False)  
products_schema = ProductSchema(many=True) 


#Routes

#Post a product
@app.route("/product",methods =['POST'])
def add_product():
    name =request.json['name']
    description =request.json['description']
    price =request.json['price']
    qty =request.json['qty']
    new_product = Product(name=name,description=description,price=price,qty=qty)
    #add data to the db
    db.session.add(new_product)
    db.session.commit()   
    return product_schema.dump(new_product)


#Get all products
@app.route("/product",methods=['GET'])
def get_products():
    all_products = Product.query.all()
    show_data = products_schema.dump(all_products)
    return show_data   


#Get  product by id
@app.route("/product/<int:id>",methods=['GET'])
def get_product_by_id(id):
    product_id = Product.query.get(id)
    if product_id is None:
      return {"404 error": "Product is not found"}  , 404
    return product_schema.dump(product_id)


#Update product
@app.route("/product/<int:id>",methods=['PUT'])
def update_product(id):
    update_product = Product.query.get_or_404(id)   

    name =request.json['name']
    description =request.json['description']
    price =request.json['price']
    qty =request.json['qty']

    update_product.name = name
    update_product.description = description
    update_product.price = price
    update_product.qty = qty
    db.session.commit()  
    return product_schema.dump(update_product)


#Delete product
@app.route("/product/<int:id>",methods=['DELETE'])
def delete_product(id):
   delete_product =  Product.query.get(id)
   if delete_product is None:
    return {"404 Error" : "Product not found"}
   db.session.delete(delete_product)
   db.session.commit()
   return {"2OO OK":"Product deleted successfully"}

#Run Server
if __name__ == '__main__':
 app.run(Debug=True)