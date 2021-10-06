from api import db
class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    profileId = db.Column(db.String(50), nullable=False, unique=True)
    gender = db.Column(db.String(15), nullable=False)
    userId = db.Column(db.String(50), db.ForeignKey('user.userId'),
        nullable=False)

    def __repr__(self) -> str:
        return '<Profile %r>' % self.profileId

    def to_dict(self):
         return {
            "userId": str(self.userId),
            "profileId": self.profileId,
            "gender": self.gender
        }

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    userId = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    profile = db.relationship('Profile', backref='profile', lazy=True)
        
    def __repr__(self) -> str:
        return '<User %r>' % self.username

    def to_dict(self):
         return {
            "userId": str(self.userId),
            "username": self.username,
            "profile": self.profile
        }