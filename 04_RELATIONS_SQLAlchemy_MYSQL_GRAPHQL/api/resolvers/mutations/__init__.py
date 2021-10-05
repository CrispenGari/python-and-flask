

# from api import db
from api.models.user import User
from api.models.profile import Profile
from uuid import uuid4
def register_user_resolver(obj, info, username, gender):

    print(username, gender)
    return {
        "userId": username,
            "username": username,
            "profile": {
                "username": "username"
            }
    }
    try:
        profile = Profile(uuid4(), gender=gender)
        db.session.add(profile)
        db.session.commit()
        user = User(
          username=username,
          userId=uuid4(),
          profile=profile  
        )
        db.session.add(user)
        db.session.commit()
        return user
    except ValueError:
       pass
    return None