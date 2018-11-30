from flask import request, jsonify, Blueprint
from my_app import app, db
from my_app.trendview.models import User
trendviewApp = Blueprint('trendview', __name__)


@trendviewApp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    telephone = request.form.get('telephone')
    password = request.form.get('password')
    newUser = User(username,email,telephone,password)
    db.session.add(newUser)
    db.session.commit()
    return "Hello"