
from api import db
from api.models import Address, Person, Profile, User
from uuid import uuid4
def register_user_resolver(obj, info, username, gender):
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


def create_person_resolver(obj, info, name):
    try:
        person = Person(name=name)
        db.session.add(person)
        db.session.commit()
        return {
            "person": person,
            "error": None
        }
    except Exception as e:
      return {
          "person":None,
          "error":{
              "field": "hello",
              "message": str(e)
          }
      }

def delete_person_resolver(obj, info, id):
    try:
        Person.query.filter_by(id=id).delete()
        db.session.commit()
        return True
    except Exception as e:
      print(e)
      return  False

def create_email_addresses(obj, info, input):
    try:
        try:
            person = Person.query.filter_by(id=input["person_id"]).first()
        except Exception as e:
             return {
                "address":None,
                "error":{
                    "field": "id",
                    "message": str(e)
                }
            }
        address = Address(email=input["email"], person_id=person.id)

        db.session.add(address)
        db.session.commit()
        return {
            "address": address,
            "error": None
        }
    except Exception as e:
      return {
          "address":None,
          "error":{
              "field": "hello",
              "message": str(e)
          }
      }

def update_email_addresses(obj, info, input):
    try:
        try:
            address = Address.query.filter_by(id=input["id"]).first()

        except Exception as e:
             return {
                "address":None,
                "error":{
                    "field": "id",
                    "message": str(e)
                }
            }

        # check the validity of the email
        address.email = input["email"]
        db.session.commit()
        return {
            "address": address,
            "error": None
        }
    except Exception as e:
      return {
          "address":None,
          "error":{
              "field": "hello",
              "message": str(e)
          }
      }