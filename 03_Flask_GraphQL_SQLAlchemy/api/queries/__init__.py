from ariadne import convert_kwargs_to_snake_case
from api.models import Post


@convert_kwargs_to_snake_case
def get_posts_resolver(obj, info):
    print("Getting all tehe posts")
    try:
        posts = [post.to_dict() for post in Post.query.all()]
        payload = {
            "success": True,
            "posts": posts
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@convert_kwargs_to_snake_case
def get_post_resolver(obj, info, postId):
    print("getting the posts of id: ", postId)
    try:
        post = Post.query.filter_by(postId=postId).first()
        payload = {
            "success": True,
            "post": post.to_dict()
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["Post item matching {id} not found"]
        }
    return payload
