from extensions import *
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


class Contact(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    full_name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    subject = db.Column(db.Text, nullable = False)
    message = db.Column(db.Text, nullable = False)

    def __init__(self, full_name,email, subject, message):
        self.full_name=full_name
        self.email=email
        self.subject=subject
        self.message=message

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    full_name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    is_superuser = db.Column(db.Boolean, nullable = True)

    def __repr__(self):
        return self.full_name

    def __init__(self, full_name,email, password, is_superuser=False):
        self.full_name=full_name
        self.email=email
        self.password=generate_password_hash(password)
        self.is_superuser=is_superuser

    def save(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# class Controller(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated
#     def not_auth(self):
#         return "NOT NOT NOT"


class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable = False)
    stock = db.Column(db.Integer(), default=0)

    def __repr__(self):
        return self.name

    def __init__(self, name):
        self.name=name

    def save(self):
        db.session.add(self)
        db.session.commit()


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    image_url = db.Column(db.String(255), nullable = False)
    name = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Integer(), nullable = False)
    low_price = db.Column(db.Integer(), nullable = False)
    stock = db.Column(db.Integer(), nullable = False)
    category_id = db.Column(db.Integer(), db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    desc = db.Column(db.Text)

    def __init__(self, image_url, name, price, low_price, stock, category_id, desc):
        self.image_url=image_url
        self.name=name
        self.price=price
        self.low_price=low_price
        self.stock=stock
        self.category_id=category_id
        self.desc = desc

    def save(self):
        db.session.add(self)
        db.session.commit()


class Reviews(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(50), nullable = False)
    message = db.Column(db.Text, nullable = False)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())

    def __init__(self, user_name, message, product_id):
        self.user_name=user_name
        self.message=message
        self.product_id=product_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class Favorites(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, user_id, product_id):
        self.user_id=user_id
        self.product_id=product_id

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def remove(self):
        db.session.delete(self)
        db.session.commit()


class Detail(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    image_url = db.Column(db.String(255), nullable = False)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, image_url, product_id):
        self.image_url=image_url
        self.product_id=product_id

    def save(self):
        db.session.add(self)
        db.session.commit()
