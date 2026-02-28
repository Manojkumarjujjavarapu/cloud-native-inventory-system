from flask import Blueprint, request, jsonify
from models.order import Order, OrderItem
from models.product import Product
from services.order_service import create_order

order_bp = Blueprint("orders", __name__)


# Create Order
@order_bp.route("/orders", methods=["POST"])
def create_order_api():
    try:
        data = request.json

        order = create_order(
            user_id=data["user_id"],
            items=data["items"]
        )

        return jsonify({
            "message": "Order created",
            "order_id": order.id
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400

# Get Order with JOIN
@order_bp.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)

    items_data = []

    for item in order.items:
        product = Product.query.get(item.product_id)

        items_data.append({
            "product_name": product.name,
            "quantity": item.quantity,
            "price": product.price
        })

    return jsonify({
        "order_id": order.id,
        "user_id": order.user_id,
        "items": items_data
    })