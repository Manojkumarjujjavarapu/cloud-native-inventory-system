import time
from flask import Flask, render_template
from sqlalchemy.exc import OperationalError

from config import Config
from extensions import db, mongo

# Import Models
from models.user import User
from models.product import Product
from models.order import Order, OrderItem
from models.inventory import Inventory

# Import Blueprints
from routes.user_routes import user_bp
from routes.log_routes import log_bp
from routes.product_routes import product_bp
from routes.order_routes import order_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    mongo.init_app(app)

    # Register Blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(log_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)

    # ======================
    # Database Connection Retry (Docker Safe)
    # ======================

    with app.app_context():

        retries = 10

        while retries > 0:
            try:
                db.create_all()
                print("✅ Database connected successfully")
                break

            except OperationalError:
                retries -= 1
                print("⏳ Waiting for database...")
                time.sleep(3)

        if retries == 0:
            print("❌ Database connection failed")

    # ======================
    # Dashboard
    # ======================

    @app.route("/")
    def dashboard():

        users = User.query.all()
        products = Product.query.all()
        orders = Order.query.all()

        logs = list(
            mongo.db.logs.find().sort("timestamp", -1).limit(10)
        )

        # Chart Data
        labels = [p.name for p in products]
        prices = [float(p.price) for p in products]

        return render_template(
            "dashboard.html",
            users=users,
            products=products,
            orders=orders,
            logs=logs,
            labels=labels,
            prices=prices,
            user_count=len(users),
            product_count=len(products),
            order_count=len(orders),
            log_count=mongo.db.logs.count_documents({})
        )

    # ======================
    # Store Page
    # ======================

    @app.route("/store")
    def store():
        products = Product.query.all()
        return render_template("store.html", products=products)

    # ======================
    # Orders History
    # ======================

    @app.route("/orders-history")
    def orders_history():

        orders = Order.query.all()
        order_data = []

        for order in orders:

            products_list = []

            for item in order.items:
                product = Product.query.get(item.product_id)

                products_list.append({
                    "name": product.name,
                    "quantity": item.quantity,
                    "price": product.price
                })

            order_data.append({
                "id": order.id,
                "created_at": order.created_at,
                "products": products_list
            })

        return render_template(
            "orders_history.html",
            orders=order_data
        )

    # ======================
    # Health Check
    # ======================

    @app.route("/health")
    def health():
        return {"status": "OK"}

    return app


app = create_app()


if __name__ == "__main__":
    print("🚀 Starting Server...")
    app.run(host="0.0.0.0", port=5001, debug=True)