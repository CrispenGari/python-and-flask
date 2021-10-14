from flask import json
from api import db
from api.models import Person, Question, User, Profile

def user_resolver(obj, info, userId):
    try:
        user = User.query.filter_by(userId=userId).first();
        return {
            "user": user,
            "error": None
        }
    except Exception as e:
        return{
            'user': None,
            "error": str(e)

        }


def person_query_resolver(obj, info, id):
    try:
        person = Person.query.filter_by(id=id).first();
        return {
            "person": person,
            "error": None
        }
    except Exception as e:
        return{
            'person': None,
            "error": str(e)

        }

def question_query_resolver(obj, info, id):
    try:
        question = Question.query.filter_by(id=id).first();
        return question
    except Exception as e:
        return None

def questions_query_resolver(obj, info):
    try:
        return Question.query.all();
    except Exception as e:
        return None