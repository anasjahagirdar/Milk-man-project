from app import db
from datetime import datetime

class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customer.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )

    quantity = db.Column(db.Integer, default=1)

    size = db.Column(db.String(10), nullable=False)

    total_price = db.Column(db.Float, nullable=False)

    order_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(20),
        default="pending"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "size": self.size,
            "total_price": self.total_price,
            "status": self.status
        }