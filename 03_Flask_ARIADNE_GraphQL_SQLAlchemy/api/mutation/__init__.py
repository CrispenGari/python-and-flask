from api import db
from datetime import date
from api.models import Post
import uuid


def create_post_resolver(obj, info, title):
    print(obj, info, title)
    try:
        post = Post(
            title=title,
            postId=uuid.uuid4(),
            createdAt=date.today()
        )
        db.session.add(post)
        db.session.commit()
        payload = {
            "success": True,
            "post": post.to_dict()
        }
    except ValueError:
        payload = {
            "success": False,
            "errors": ["something happenned."]
        }
    return payload


def update_post_resolver(obj, info, postId, title):
    try:
        post = Post.query.filter_by(postId=postId).first()
        if post:
            post.title = title
        db.session.add(post)
        db.session.commit()
        payload = {
            "success": True,
            "post": post.to_dict()
        }

    except AttributeError:
        payload = {
            "success": False,
            "errors": ["item matching id {id} not found"]
        }
    return payload


def delete_post_resolver(obj, info, postId):
    try:
        post = Post.query.filter_by(postId=postId).first()
        db.session.delete(post)
        db.session.commit()
        payload = True
    except AttributeError:
        payload = False
    return payload
