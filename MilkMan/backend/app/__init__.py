from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy import text
import config

db = SQLAlchemy()
jwt = JWTManager()


def create_app():

    app = Flask(
        __name__,
        static_folder='../static',        # images live in backend/static/, not backend/app/static/
        static_url_path='/static'
    )
    app.config.from_object(config)

    CORS(
        app,
        resources={r"/api/*": {"origins": config.CORS_ORIGINS}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "X-CSRF-TOKEN"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
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
                        p_alters.append("ALTER TABLE product ADD COLUMN unit VARCHAR(50) DEFAULT '500ml'")
                    if "is_active" not in prod_cols:
                        p_alters.append("ALTER TABLE product ADD COLUMN is_active BOOLEAN DEFAULT 1")
                    if "image_url" not in prod_cols:
                        p_alters.append("ALTER TABLE product ADD COLUMN image_url VARCHAR(500)")
                    for stmt in p_alters:
                        conn.execute(text(stmt))
                    if p_alters:
                        conn.commit()

                cust_cols = {
                    row[1]
                    for row in conn.execute(text("PRAGMA table_info(customer)")).fetchall()
                }
                if cust_cols:
                    c_alters = []
                    if "is_active" not in cust_cols:
                        c_alters.append("ALTER TABLE customer ADD COLUMN is_active BOOLEAN DEFAULT 1")
                    for stmt in c_alters:
                        conn.execute(text(stmt))
                    if c_alters:
                        conn.commit()

                staff_cols = {
                    row[1]
                    for row in conn.execute(text("PRAGMA table_info(staff)")).fetchall()
                }
                if staff_cols:
                    s_alters = []
                    if "is_active" not in staff_cols:
                        s_alters.append("ALTER TABLE staff ADD COLUMN is_active BOOLEAN DEFAULT 1")
                    for stmt in s_alters:
                        conn.execute(text(stmt))
                    if s_alters:
                        conn.commit()

                admin_cols = {
                    row[1]
                    for row in conn.execute(text("PRAGMA table_info(admin)")).fetchall()
                }
                if admin_cols:
                    a_alters = []
                    if "is_active" not in admin_cols:
                        a_alters.append("ALTER TABLE admin ADD COLUMN is_active BOOLEAN DEFAULT 1")
                    for stmt in a_alters:
                        conn.execute(text(stmt))
                    if a_alters:
                        conn.commit()

                order_cols = {
                    row[1]
                    for row in conn.execute(text('PRAGMA table_info("order")')).fetchall()
                }
                if order_cols:
                    o_alters = []
                    if "subscription_id" not in order_cols:
                        o_alters.append("ALTER TABLE \"order\" ADD COLUMN subscription_id INTEGER")
                    if "amount" not in order_cols:
                        o_alters.append("ALTER TABLE \"order\" ADD COLUMN amount FLOAT")
                    if "delivered_at" not in order_cols:
                        o_alters.append("ALTER TABLE \"order\" ADD COLUMN delivered_at DATETIME")
                    for stmt in o_alters:
                        conn.execute(text(stmt))
                    if o_alters:
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

    from app.routes.subscription import subscription_bp
    app.register_blueprint(subscription_bp, url_prefix="/api/subscriptions")

    # -------- GLOBAL ERROR HANDLERS --------

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    @app.route("/")
    def home():
        return jsonify({"message": "MilkMan API running", "version": "2.0"})

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "service": "backend-service"}), 200

    return app
