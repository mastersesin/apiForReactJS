from my_app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    telephone = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, username, email, telephone, password):
        self.username = username
        self.email = email
        self.telephone = telephone
        self.password = password

    def __repr__(self):
        return '<User %d>' % self.id