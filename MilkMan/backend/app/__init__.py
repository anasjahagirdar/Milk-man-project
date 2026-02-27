from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy import text
import config

db = SQLAlchemy()
jwt = JWTManager()


def create_app():

    app = Flask(__name__)
    app.config.from_object(config)

    CORS(
        app,
        resources={r"/api/*": {"origins": config.CORS_ORIGINS}},
        supports_credentials=True,
    )
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        if db.engine.dialect.name == "sqlite":
            conn = db.engine.connect()
            try:
                existing = {
                    row[1]
                    for row in conn.execute(text("PRAGMA table_info(subscription)")).fetchall()
                }
                if existing:
                    alters = []
                    if "frequency" not in existing:
                        alters.append(
                            "ALTER TABLE subscription ADD COLUMN frequency VARCHAR(20) DEFAULT 'daily'"
                        )
                    if "status" not in existing:
                        alters.append(
                            "ALTER TABLE subscription ADD COLUMN status VARCHAR(20) DEFAULT 'active'"
                        )
                    if "paused_until" not in existing:
                        alters.append("ALTER TABLE subscription ADD COLUMN paused_until DATE")
                    if "canceled_at" not in existing:
                        alters.append("ALTER TABLE subscription ADD COLUMN canceled_at DATETIME")
                    if "unit_price" not in existing:
                        alters.append("ALTER TABLE subscription ADD COLUMN unit_price FLOAT")
                    if "updated_at" not in existing:
                        alters.append("ALTER TABLE subscription ADD COLUMN updated_at DATETIME")
                    for stmt in alters:
                        conn.execute(text(stmt))
                    if alters:
                        conn.commit()

                prod_cols = {
                    row[1]
                    for row in conn.execute(text("PRAGMA table_info(product)")).fetchall()
                }
                if prod_cols:
                    p_alters = []
                    if "unit" not in prod_cols:
                        p_alters.append("ALTER TABLE product ADD COLUMN unit VARCHAR(20) DEFAULT 'custom'")
                    if "is_active" not in prod_cols:
                        p_alters.append("ALTER TABLE product ADD COLUMN is_active BOOLEAN DEFAULT 1")
                    if "size" in prod_cols:
                        # SQLite cannot alter column type; keep existing 'size' col and accept longer values by app-level
                        pass
                    for stmt in p_alters:
                        conn.execute(text(stmt))
                    if p_alters:
                        conn.commit()
            finally:
                conn.close()

    @jwt.unauthorized_loader
    def _unauthorized(reason):
        return jsonify({"error": "Authentication required"}), 401

    @jwt.invalid_token_loader
    def _invalid_token(reason):
        return jsonify({"error": "Invalid authentication token"}), 401

    @jwt.expired_token_loader
    def _expired_token(jwt_header, jwt_payload):
        return jsonify({"error": "Authentication token expired"}), 401

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
