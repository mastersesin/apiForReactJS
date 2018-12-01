from flask import request, jsonify, Blueprint
from my_app import app, db
from my_app.trendview.models import User
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
trendviewApp = Blueprint('trendview', __name__)

returnMsg = {
    "registerSuccess":{
        "code":1,"msg":"User created successfully."
    },
    "Phone Duplicated":{
        "code":2,"msg":"Phone number has been used by another user."
    },
    "Email Duplicated":{
        "code":3,"msg":"Email address has been used by another user."
    },
    "Username Duplicated":{
        "code":4,"msg":"Username has been used by another user."
    },
    "Username or Password Incorrect":{
        "code":5,"msg":"Username or Password Incorrect"
    },
    "Return Token":{
        "code":6,"msg":""
    }
}

@trendviewApp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    telephone = request.form.get('telephone')
    password = request.form.get('password')
    referer = request.form.get('referer')
    duplicateUsernameCheck = User.query.filter_by(username=username).first()
    if duplicateUsernameCheck == None:
        duplicateEmailCheck = User.query.filter_by(email=email).first()
        if duplicateEmailCheck == None:
            duplicatePhoneNumberCheck = User.query.filter_by(telephone=telephone).first()
            if duplicatePhoneNumberCheck == None:
                newUser = User(username, email, telephone, password, referer)
                db.session.add(newUser)
                db.session.commit()
                return jsonify(returnMsg["registerSuccess"])
            else:
                return jsonify(returnMsg["Phone Duplicated"])
        else:
            return jsonify(returnMsg["Email Duplicated"])
    else:
        return jsonify(returnMsg["Username Duplicated"])

@trendviewApp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    usernameCheck = User.query.filter_by(username=username).first()
    if usernameCheck != None:
        passwordCheck = usernameCheck.password
        if passwordCheck == password:
            msg = returnMsg["Return Token"]
            msg['msg'] = usernameCheck.generate_auth_token()
            return jsonify(msg)
        else:
            return jsonify(returnMsg["Username or Password Incorrect"])
    else:
        return jsonify(returnMsg["Username or Password Incorrect"])

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