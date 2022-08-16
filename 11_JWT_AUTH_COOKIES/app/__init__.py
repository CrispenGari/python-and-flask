from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
app = Flask(__name__)
app.secret_key = "abcd"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=7)
db = SQLAlchemy(app)