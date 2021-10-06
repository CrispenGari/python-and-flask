
from api import db
from api.models import Profile, User
from uuid import uuid4
def register_user_resolver(obj, info, username, gender):
    print(username, gender)
    try:
        user = User(
          username=username,
          userId=uuid4()
        )
        db.session.add(user)
        db.session.commit()
        profile = Profile(
            profileId=uuid4(),
            gender=gender, 
            userId=user.userId
         )
        db.session.add(profile)
        db.session.commit()
        return {
            "user": user.to_dict(),
            "error": None
        }
    except Exception as e:
      return {
          "user":None,
          "error":{
              "field": "hello",
              "message": str(e)
          }
      }