from app import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
        nullable=False
    )

    size = db.Column(db.String(10), nullable=False)  # 0.5L, 1L, 2L
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    stock = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category_id": self.category_id,
            "size": self.size,
            "price": self.price,
            "description": self.description,
            "stock": self.stock
        }