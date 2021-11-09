
from api import db
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    userId = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    # profile = db.relationship('Profile', backref='profile', lazy=True, uselist=False)

    def __repr__(self) -> str:
        return '<User %r>' % self.username