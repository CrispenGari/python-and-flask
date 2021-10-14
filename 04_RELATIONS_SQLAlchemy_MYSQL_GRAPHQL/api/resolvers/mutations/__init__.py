from api import db
from api.models import Address, Category, Person, Profile, Question, User
from uuid import uuid4

def register_user_resolver(obj, info, username):
    print("username", username)
    try:
        user = User(
          username=username,
          userId=uuid4()
        )
        db.session.add(user)
        db.session.commit()
        print(user.to_dict())
        return {
            "user": user,
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

def create_profile_resolver(obj, info, gender, userId):
    try:
        profile = Profile(
            profileId=uuid4(),
            gender=gender, 
            userId=userId
         )
        db.session.add(profile)
        db.session.commit()
        return {
            "profile": profile,
            "error": None
        }
    except Exception as e:
      return {
          "profile":None,
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
        person = Person.query.filter_by(id=id).first()
        db.session.delete(person)
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


def create_question_resolver(obj, info, question):
    try:
        qn = Question(question=question)
        db.session.add(qn)
        db.session.commit()
        return qn
    except Exception as e:
      return None

def create_category_resolver(obj, info, category, questionId):
    try:
        try:
            question = Question.query.filter_by(id=questionId).first()
        except:
            return {
                "category": None
            }

        cate = Category(category=category)
        db.session.add(cate)
        question.categories.append(cate)
        db.session.add(cate)
        db.session.commit()
        return cate
    except Exception as e:
      return None
