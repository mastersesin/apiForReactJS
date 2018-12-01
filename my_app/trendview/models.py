from my_app import db,app
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    telephone = db.Column(db.String(255))
    password = db.Column(db.String(255))
    point = db.Column(db.Integer)
    referer = db.Column(db.String(255))

    def __init__(self, username, email, telephone, password, referer):
        self.username = username
        self.email = email
        self.telephone = telephone
        self.password = password
        self.point = 0
        self.referer = referer
    def __repr__(self):
        return '<User %d>' % self.id

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=60*60*2)
        return (s.dumps({'id': self.id})).decode("utf-8")