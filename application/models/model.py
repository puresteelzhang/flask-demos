# -*- coding: utf-8 -*-

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from application.extensions import db, login_manager

__all__ = ['Book', 'User']


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)

    @property
    def password(self):
        raise AttributeError('')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Book(db.Model):
    """data model"""
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    posted_on = db.Column(db.Date, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(Book, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<Book '%s'>" % self.title

    def store_to_db(self):
        """save to database"""

        db.session.add(self)
        db.session.commit()

    def delete_book(self):
        """delete data"""

        db.session.delete(self)
        db.session.commit()
