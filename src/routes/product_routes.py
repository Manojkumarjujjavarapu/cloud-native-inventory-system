from flask import Blueprint, request, jsonify
from extensions import db
from models.product import Product
from models.inventory import Inventory
from services.log_service import log_activity

product_bp = Blueprint("products", __name__)

 
# Create Product
@product_bp.route("/products", methods=["POST"])
def create_product():
    data = request.json

    product = Product(
        name=data["name"],
        price=data["price"],
        image_url=data.get("image_url")
    )

    db.session.add(product)
    db.session.commit()

    # Create inventory record
    inventory = Inventory(
        product_id=product.id,
        stock=data.get("stock", 0)
    )

    db.session.add(inventory)
    db.session.commit()

    log_activity("CREATE_PRODUCT", data)

    return jsonify(product.to_dict()), 201


# Get Products
@product_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


# Update Product Price
@product_bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)

    data = request.json
    product.price = data["price"]

    db.session.commit()

    log_activity("UPDATE_PRODUCT", {"product_id": product_id})

    return jsonify(product.to_dict())


# Delete Product
@product_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    log_activity("DELETE_PRODUCT", {"product_id": product_id})

    return {"message": "Product deleted"}