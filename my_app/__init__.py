from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:st!xadminHY@11.11.11.9/new_schema'
app.config['SECRET_KEY'] = 'trantrongtyckiuzk4ever!@#!!!@@##!*&%^$$#$'
db = SQLAlchemy(app)
from my_app.trendview.views import trendviewApp
app.register_blueprint(trendviewApp)
db.create_all()