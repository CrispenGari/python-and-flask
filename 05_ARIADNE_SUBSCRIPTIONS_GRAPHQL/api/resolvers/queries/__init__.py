from flask import json
from api import db

from ariadne import QueryType

from api.models import Post
query = QueryType()

@query.field("hello")
def hello_world_resolver(obj, info):
   return "hello, world"

@query.field("getPosts")
def get_posts_resolver(obj, info):
    try:
        posts = Post.query.all()
        return{
            "error": None,
            "posts": posts
        }
    except Exception as e:
        return{
        "error": {"message":str(e), "field": "unknown"},
        "posts": None
        }

@query.field("getPost")
def get_post_resolver(obj, info, postId):
    try:
        post = Post.query.filter_by(postId=postId).first()
        if post == None:
            raise Exception("there's no post of that id.")
        return{
            "error": None,
            "post": post
        }
    except Exception as e:
        return{
        "error": {"message":str(e), "field": "id"},
        "posts": None
        }
