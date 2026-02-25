from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import config

db = SQLAlchemy()
jwt = JWTManager()


def create_app():

    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    # -------- REGISTER ROUTES --------

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    from app.routes.customer import customer_bp
    app.register_blueprint(customer_bp, url_prefix="/api/customers")

    from app.routes.staff import staff_bp
    app.register_blueprint(staff_bp, url_prefix="/api/staff")

    from app.routes.category import category_bp
    app.register_blueprint(category_bp, url_prefix="/api/categories")

    from app.routes.product import product_bp
    app.register_blueprint(product_bp, url_prefix="/api/products")

    from app.routes.order import order_bp
    app.register_blueprint(order_bp, url_prefix="/api/orders")

    # ---------------------------------

    from app.routes.subscription import subscription_bp
    app.register_blueprint(subscription_bp, url_prefix="/api/subscriptions")

    @app.route("/")
    def home():
        return jsonify({"message": "MilkMan API running"})

    return app