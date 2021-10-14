from api import db
from uuid import uuid4
from ariadne import MutationType

from api.models import Post
mutation = MutationType()

@mutation.field("createPost")
def create_post_resolver(obj, info, input):
    try:
        post = Post(postId=uuid4(), caption=input["caption"])
        db.session.add(post)
        db.session.commit()
        return{
            "error": None,
            "post": post
        }
    except Exception as e:
        return{
            "error": {"message":str(e), "field": "unknown"},
            "post": None
        }