from extensions import db
from models.order import Order, OrderItem
from models.inventory import Inventory
from services.log_service import log_activity


def create_order(user_id, items):
    """
    items = [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 1}
    ]
    """

    order = Order(user_id=user_id)
    db.session.add(order)
    db.session.commit()

    for item in items:
        product_id = item["product_id"]
        quantity = item["quantity"]

        # Check inventory
        inventory = Inventory.query.filter_by(product_id=product_id).first()

        if not inventory or inventory.stock < quantity:
            raise Exception("Insufficient stock")

        # Deduct stock
        inventory.stock -= quantity

        order_item = OrderItem(
            order_id=order.id,
            product_id=product_id,
            quantity=quantity
        )

        db.session.add(order_item)

    db.session.commit()

    # Log in MongoDB
    log_activity("CREATE_ORDER", {
        "order_id": order.id,
        "user_id": user_id,
        "items": items
    })

    return order