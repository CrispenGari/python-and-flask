from api import db
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    userId = db.Column(db.String(50), nullable=False, unique=True)
    bio = db.Column(db.String(50), nullable=True, unique=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False, unique=False)

    def __init__(self, userId, username, password, bio=None) -> None:
        self.userId = userId
        self.username = username
        self.bio = bio
        self.password = password

    def __repr__(self) -> str:
        return '<User %r>' % self.username