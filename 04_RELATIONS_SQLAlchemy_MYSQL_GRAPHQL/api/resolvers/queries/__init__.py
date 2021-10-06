from api import db
from models import User, Profile

def create_post_resolver(obj, info, title):
    try:
        user = User(
            
        )
        # post = Post(
        #     title=title,
        #     postId=uuid.uuid4(),
        #     createdAt=date.today()
        # )
        # db.session.add(post)
        # db.session.commit()
        # payload = {
        #     "success": True,
        #     "post": post.to_dict()
        # }
    except ValueError:
        payload = {
            "success": False,
            "errors": ["something happenned."]
        }
    return payload