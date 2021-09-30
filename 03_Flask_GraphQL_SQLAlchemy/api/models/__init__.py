from api import db

class Post(db.Model):
    # database column
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # the id that we will expose to the user
    postId = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.Date)

    def to_dict(self):
        return {
            "postId": self.postId,
            "title": self.title,
            "createdAt": str(self.created_at.strftime('%d-%m-%Y'))
        }