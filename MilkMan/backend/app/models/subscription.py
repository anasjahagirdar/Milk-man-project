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

    frequency = db.Column(db.String(20), default="daily")

    status = db.Column(db.String(20), default="active")
    paused_until = db.Column(db.Date)
    canceled_at = db.Column(db.DateTime)

    unit_price = db.Column(db.Float)

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

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "quantity": self.quantity,
            "frequency": self.frequency,
            "status": self.status,
            "paused_until": self.paused_until.isoformat() if self.paused_until else None,
            "unit_price": self.unit_price,
            "payment_status": self.payment_status
        }
