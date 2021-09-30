from api import db
from datetime import date
from ariadne import convert_kwargs_to_snake_case
from api.models import Post
import uuid


@convert_kwargs_to_snake_case
def create_post_resolver(obj, info, title):
    try:
        today = date.today()
        post = Post(
            title=title,
            postId=uuid.uuid4(),
            created_at=today.strftime("%b-%d-%Y")
        )
        print("creating a post .....................")
        print(post)

        print("0" * 50)
        db.session.add(post)
        db.session.commit()
        payload = {
            "success": True,
            "post": post.to_dict()
        }
    except ValueError:
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }
    return payload


@convert_kwargs_to_snake_case
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


@convert_kwargs_to_snake_case
def delete_post_resolver(obj, info, postId):
    try:
        post = Post.query.filter_by(postId=postId).first()
        db.session.delete(post)
        db.session.commit()
        payload = {"success": True, "post": true}
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not found"]
        }
    return payload
