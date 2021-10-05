from api import db
class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    profileId = db.Column(db.String(50), nullable=False, unique=True)
    gender = db.Column(db.String(15), nullable=False, unique=True)
    userId = db.Column(db.String(50), db.ForeignKey('users.userId'),
        nullable=False)

    def __init__(self, profileId: str, gender: str) -> None:
        self.gender = gender
        self.profileId = profileId
        super().__init__()


    def __repr__(self) -> str:
        return '<Profile %r>' % self.profileId

    def to_dict(self):
         return {
            "userId": str(self.userId),
            "profileId": self.profileId,
            "gender": self.gender
        }