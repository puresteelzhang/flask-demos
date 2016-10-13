# -*- coding: utf-8 -*-

from application.extensions import db
from datetime import datetime

__all__ = ['Book']


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
