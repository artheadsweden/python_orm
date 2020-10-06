from config import *
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    email_addresses = db.relationship('EmailAddress', backref='user')
    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        d = dict(id=self.id, username=self.username, created=str(self.created))
        d['email_addresses'] = [address.to_dict() for address in self.email_addresses]
        return d


class EmailAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return dict(email=self.email)