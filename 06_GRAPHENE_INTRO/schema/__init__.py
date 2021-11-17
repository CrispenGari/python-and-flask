
from uuid import uuid4

from api import db
from graphene import ObjectType,  Schema
import graphene
from models import User as UserModel


class UserType(ObjectType):
    """
    This class contains the fields that we are interested in
    working with on the user model
    """
    userId = graphene.String(required=True)
    username = graphene.String(required=True)
    bio = graphene.String(required=False)
    # Note: the password field is not going to be exposed to the api


class ErrorType(ObjectType):
    """
    This is the error type
    """
    field = graphene.String(required=True)
    message = graphene.String(required = True)

class UserResponse(ObjectType):
    """
    This class object is the object type that will return the 
    user data we are interested in
    """
    error = graphene.Field(ErrorType, required=False)
    ok = graphene.Boolean(required=True)
    user = graphene.Field(UserType, required=False)

class UsersResponse(ObjectType):
    """
    This class contains the user response object type 
    """
    error = graphene.Field(ErrorType, required=False)
    ok = graphene.Boolean(required=True)
    total = graphene.Int(required=True)
    users = graphene.List(UserType, required=False)


class UserCreateInputType(graphene.InputObjectType):
    username = graphene.String(required=True)
    bio = graphene.String(required=False)
    password = graphene.String(required=True)
class UserFindInputType(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)



# Mutations Classes

class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserCreateInputType(required=True)

    user = graphene.Field(lambda: UserResponse)
    def mutate(root, args, input):
        if len(input.username) < 3:
            user = UserResponse(
                ok = False,
                error = ErrorType(message="username must be at least 3 characters", field="username"),
                user = None
            )
            return CreateUser(user)
        
        if len(input.password) < 3:
            user = UserResponse(
                ok = False,
                error = ErrorType(message="password must be at least 3 characters", field="password"),
                user = None
            )
            return CreateUser(user)

        _user = UserModel.query.filter_by(username=input.username).first()
        if _user:
            user = UserResponse(
                ok = False,
                error = ErrorType(message="username is taken", field="username"),
                user = None
            )
            return CreateUser(user)

        __user = UserModel(
            userId= uuid4(),
            username = input.username,
            password = input.password,
            bio = input.bio
        )
        db.session.add(__user)
        db.session.commit()
        user = UserResponse(
                ok = True,
                error = None,
                user = __user
            )
        return CreateUser(user)   



class FindUser(graphene.Mutation):
    class Arguments:
        input = UserFindInputType(required=True)

    user = graphene.Field(lambda: UserResponse)
    def mutate(root, args, input):
        _user = UserModel.query.filter_by(username=input.username).first()
        if not _user:
            user = UserResponse(
                ok = False,
                error = ErrorType(message="invalid username", field="username"),
                user = None
            )
            return FindUser(user)

        if _user.password != input.password:
            user = UserResponse(
                ok = False,
                error = ErrorType(message="password is incorrect", field="password"),
                user = None
            )
            return FindUser(user)

        user = UserResponse(
                ok = True,
                error = None,
                user = _user
        )
        return FindUser(user)   


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    find_user = FindUser.Field()

class Query(ObjectType):
    users = graphene.Field(graphene.NonNull(UsersResponse))
    def resolve_users(root, info):
        res = UserModel.query.all()
        _len = len(res)
        ok = True
        return UsersResponse(
            ok =ok,
            total = _len,
            users = res,
            error= None
        )
schema = Schema(query=Query, mutation=Mutation)