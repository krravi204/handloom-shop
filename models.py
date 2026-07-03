from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Saree, Kurta, Shirt, Stole
    material = db.Column(db.String(50), nullable=False)  # Cotton, Silk, Linen, Khadi
    weave = db.Column(db.String(50), nullable=False)     # Ikat, Banarasi, Jamdani, Handloom-Plain
    stock = db.Column(db.Integer, default=10, nullable=False)
    featured = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'category': self.category,
            'material': self.material,
            'weave': self.weave,
            'stock': self.stock,
            'featured': self.featured
        }

class Order(db.Model):
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)  # Pending, Processing, Shipped, Delivered, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Cascade delete so if an order is deleted, its items are too
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price of product at checkout
    
    # Relationship to product
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

class StoreSettings(db.Model):
    __tablename__ = 'store_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(100), nullable=False)
    store_tagline = db.Column(db.String(150), nullable=False)
    primary_color = db.Column(db.String(7), nullable=False)  # Hex code (e.g., #A24B31)
    alert_bar_text = db.Column(db.String(200), nullable=False)
    hero_title = db.Column(db.String(150), nullable=False)
    hero_subtitle = db.Column(db.String(150), nullable=False)
    hero_description = db.Column(db.Text, nullable=False)
    free_shipping_threshold = db.Column(db.Float, default=1999.00, nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    contact_phone = db.Column(db.String(30), nullable=False)
    contact_address = db.Column(db.Text, nullable=False)

class Subscriber(db.Model):
    __tablename__ = 'subscriber'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
