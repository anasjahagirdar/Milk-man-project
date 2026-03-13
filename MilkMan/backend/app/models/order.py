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

    subscription_id = db.Column(
        db.Integer,
        db.ForeignKey("subscription.id"),
        nullable=True
    )

    quantity = db.Column(db.Integer, default=1)
    amount = db.Column(db.Float, nullable=False)

    # kept for backward compat — now optional
    size = db.Column(db.String(50), nullable=True)
    total_price = db.Column(db.Float, nullable=True)

    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    delivered_at = db.Column(db.DateTime, nullable=True)

    status = db.Column(db.String(20), default="pending")

    product = db.relationship("Product", backref=db.backref("orders", lazy=True))

    def __repr__(self):
        return f"<Order {self.id} customer={self.customer_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "subscription_id": self.subscription_id,
            "quantity": self.quantity,
            "amount": self.amount or self.total_price or 0,
            "total_price": self.total_price or self.amount or 0,
            "status": self.status,
            "order_date": self.order_date.isoformat() if self.order_date else None,
            "delivered_at": self.delivered_at.isoformat() if self.delivered_at else None,
            "product_name": self.product.name if self.product else None,
        }