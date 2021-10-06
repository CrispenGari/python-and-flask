from flask import json
from api import db
from api.models import User, Profile

def user_resolver(obj, info, userId):
    try:
        user = User.query.filter_by(userId=userId).first();
        return {
            "user": user.to_dict(),
            "error": None
        }
    except Exception as e:
        return{
            'user': None,
            "error": str(e)

        }

def profile_resolver(obj, info, profileId):
    try:
        profile = Profile.query.filter_by(profileId=profileId).first()
        return{
            "profile": profile.to_dict(),
            "error": None
        }
    except Exception as e:
        return{
            'profile': None,
            "error": str(e)

        }