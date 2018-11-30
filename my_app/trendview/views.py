from flask import request, jsonify, Blueprint
from my_app import app, db
from my_app.trendview.models import User
trendviewApp = Blueprint('trendview', __name__)

returnMsg = {
    "registerSuccess":{"code":1,"msg":"User created"}
}

@trendviewApp.route('/register', methods=['POST'])
def register():
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