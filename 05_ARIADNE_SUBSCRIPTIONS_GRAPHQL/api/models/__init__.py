from api import db
from sqlalchemy.sql import func

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255), nullable=False)
    createdAt = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return "<Post %r>", self.caption
