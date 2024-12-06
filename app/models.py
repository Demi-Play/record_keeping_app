from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='client')  # admin, moderator, client

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    min_level = db.Column(db.Integer, nullable=False)
    max_level = db.Column(db.Integer, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))

    def update_quantity(self, change_quantity, reason):
        """Обновляет количество товара и записывает изменение в историю."""
        self.quantity += change_quantity
        change_record = InventoryChangeHistory(
            item_id=self.id,
            change_date=datetime.now(),
            changed_quantity=change_quantity,
            reason=reason
        )
        db.session.add(change_record)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(20), default='new')
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_item.id'))  # Связь с товаром
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))  # Связь с поставщиком

    item = db.relationship('InventoryItem', backref='orders')  # Связь с товаром
    supplier = db.relationship('Supplier', backref='orders')  # Связь с поставщиком

class InventoryChangeHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_item.id'))
    change_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    changed_quantity = db.Column(db.Integer)
    reason = db.Column(db.String(200))