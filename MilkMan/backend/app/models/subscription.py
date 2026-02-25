from app import db
from datetime import datetime

class Subscription(db.Model):

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

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

    quantity = db.Column(db.Integer, default=1)

    payment_status = db.Column(
        db.String(20),
        default="pending"
    )

    payment_updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    notes = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "payment_status": self.payment_status
        }