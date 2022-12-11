
from api.models import Post
def get_posts_resolver(obj, info):
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



def get_post_resolver(obj, info, postId):
    print("getting the posts of id: ", postId)
    try:
        post = Post.query.filter_by(postId=postId).first()
        payload = {
            "success": True,
            "post": post.to_dict()
        }
    except:  # todo not found
        payload = {
            "success": False,
            "errors": ["Post item matching {postId} not found"]
        }
    return payload
