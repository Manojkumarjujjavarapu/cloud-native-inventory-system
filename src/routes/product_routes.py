from flask import Blueprint, request, jsonify, render_template, redirect
from extensions import db
from models.product import Product
from models.inventory import Inventory
from services.log_service import log_activity
from utils.auth import admin_required


product_bp = Blueprint("products", __name__)


# =========================
# API — Create Product
# =========================
@product_bp.route("/products", methods=["POST"])
@admin_required
def create_product():
    data = request.json

    product = Product(
        name=data["name"],
        price=data["price"],
        image_url=data.get("image_url")
    )

    db.session.add(product)
    db.session.commit()

    inventory = Inventory(
        product_id=product.id,
        stock=data.get("stock", 0)
    )

    db.session.add(inventory)
    db.session.commit()

    log_activity("CREATE_PRODUCT", data)

    return jsonify(product.to_dict()), 201


# =========================
# API — Get Products
# =========================
@product_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


# =========================
# API — Update Product
# =========================
@product_bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)

    data = request.json
    product.price = data["price"]

    db.session.commit()

    log_activity("UPDATE_PRODUCT", {"product_id": product_id})

    return jsonify(product.to_dict())


# =========================
# API — Delete Product
# =========================
@product_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    log_activity("DELETE_PRODUCT", {"product_id": product_id})

    return {"message": "Product deleted"}


# =========================
# UI — Add Product Page
# =========================
@product_bp.route("/products/add", methods=["GET"])
def add_product_page():
    return render_template("add_product.html")


# =========================
# UI — Save Product from Form
# =========================
@product_bp.route("/products/add", methods=["POST"])
def add_product():

    name = request.form["name"]
    price = float(request.form["price"])
    stock = int(request.form["stock"])
    image_url = request.form.get("image_url")

    product = Product(
        name=name,
        price=price,
        image_url=image_url
    )

    db.session.add(product)
    db.session.commit()

    inventory = Inventory(
        product_id=product.id,
        stock=stock
    )

    db.session.add(inventory)
    db.session.commit()

    log_activity("CREATE_PRODUCT_UI", {"name": name})

    return redirect("/store")