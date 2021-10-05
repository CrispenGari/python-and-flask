
from api import db
from api.models.profile import Profile
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    userId = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    profile = db.relationship('profile', backref='profiles', lazy=True)

    def __init__(self, userId: str, username: str, profile: Profile) -> None:
        self.userId = userId,
        self.username= username
        self.profile = profile
        
    def __repr__(self) -> str:
        return '<User %r>' % self.username

    def to_dict(self):
         return {
            "userId": str(self.userId),
            "username": self.username,
            "profile": self.profile.to_dict()
        }