from flask import request, jsonify, Blueprint
from my_app import app, db
from my_app.trendview.models import User
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
trendviewApp = Blueprint('trendview', __name__)

returnMsg = {
    "registerSuccess":{"code":1,"msg":"User created"}
}

@trendviewApp.route('/register', methods=['POST'])
def register():
    print(request.__dict__)
    username = request.form.get('username')
    email = request.form.get('email')
    telephone = request.form.get('telephone')
    password = request.form.get('password')
    duplicateUsernameCheck = User.query.filter_by(username=username).first()
    if duplicateUsernameCheck == None:
        duplicateEmailCheck = User.query.filter_by(email=email).first()
        if duplicateEmailCheck == None:
            duplicatePhoneNumberCheck = User.query.filter_by(telephone=telephone).first()
            if duplicatePhoneNumberCheck == None:
                newUser = User(username, email, telephone, password)
                db.session.add(newUser)
                db.session.commit()
                return jsonify(returnMsg['registerSuccess'])
            else:
                return "Phone Duplicated"
        else:
            return "Email Duplicated"
    else:
        return "Username Duplicated"

@trendviewApp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    usernameCheck = User.query.filter_by(username=username).first()
    if usernameCheck != None:
        passwordCheck = usernameCheck.password
        if passwordCheck == password:
            return usernameCheck.generate_auth_token()
        else:
            return "Username or Password Incorrect"
    else:
        return "Username or Password Incorrect"

def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token
    user = User.query.get(data['id'])
    return user