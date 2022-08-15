from datetime import timedelta
from flask import Flask

app = Flask(__name__)

app.secret_key = "abcd"
"""
If SQLALCHEMY_DATABASE_URI is a relative path then we should use 3 slashes
for the uri otherwise 4 slashes.
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=7)