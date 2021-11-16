
from os import error
from uuid import uuid4
from api import db
from graphene import ObjectType,  Schema, relay
import graphene
from graphene.types import field, uuid
from models import User as UserModel
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )




# Todo CRUD OPERATIONS
todos = list()

class Todo(ObjectType):
    title = graphene.String(required=True)
    completed= graphene.Boolean(required=True, default_value=False)
    description = graphene.String(required=False)
    id = graphene.Int(required=True)

class TodoInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    completed= graphene.Boolean(required=True, default_value=False)
    description = graphene.String(required=False)

class TodoResponse(ObjectType):
    error= graphene.String(required=False)
    todo = graphene.Field(Todo)

class CreateTodo(graphene.Mutation):
    class Arguments:
        input_ = TodoInput(required=True)

    ok = graphene.Boolean()
    todo = graphene.Field(lambda: Todo)
    def mutate(root, info, input_=None):
        todo = Todo(
            title = input_.title,
            completed = input_.completed,
            description = input_.description,
            id = len(todos)
        )
        ok = True
        todos.append(todo)
        return CreateTodo(ok=ok, todo=todo)
    
class UpdateTodo(graphene.Mutation):
    class Arguments:
        input_ = TodoInput(required=True)
        id = graphene.Int(required=True)

    ok = graphene.Boolean()
    todo = graphene.Field(lambda: Todo)

    def mutate(root, info, input_=None, id=None):
        try:
            todo = list(filter(lambda x: x.id == id, todos))[0]
            index = todos.index(todo)
            todo = Todo(
                title = input_.title,
                completed = input_.completed,
                description = input_.description,
                id = id
            )
            todos[index] = todo
            return UpdateTodo(ok=True, todo=todo)
        except:
            return UpdateTodo(ok=False, todo=None)

class DeleteTodo(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()
    def mutate(root, info, id=None):
        global todos
        try:
            todos = list(filter(lambda x: x.id != id, todos))
            return DeleteTodo(ok=True)
        except:
            return DeleteTodo(ok=False)


class UserInput(graphene.InputObjectType):
    username = graphene.String(required=True)

class AddUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    user = graphene.Field(lambda: User)
    ok = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, input):
        user = UserModel(uuid4(), input["username"])
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return AddUser(user=None, ok=False, error=e)
        return AddUser(user=user, ok=True, error=None)

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
    ok = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, id):
        user = UserModel.query.filter_by(userId=id).first()
        if not user:
            return AddUser(ok=False, error="the username with that id does not exists.")
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            return AddUser( ok=False, error=str(error))
        return AddUser(ok=True, error=None)

        

class Mutation(ObjectType):
    create_todo = CreateTodo.Field(
        name="create_todo",
        description="creating todos"
    )
    delete_todo = DeleteTodo.Field()
    update_todo = UpdateTodo.Field()
    add_user = AddUser.Field()
    delete_user = DeleteUser.Field()
class Query(ObjectType):
    node = relay.Node.Field() # required
    todos = graphene.List(graphene.NonNull(Todo))
    todo = graphene.Field(TodoResponse, id=graphene.Int(required=True))
    hello = graphene.String()

    users = SQLAlchemyConnectionField(User)

    def resolve_todos(root, info):
        return todos

    def resolve_hello(root, info):
        return "hello world"

    def resolve_todo(root, info, id):
        try:
            todo = list(filter(lambda x: x.id == id, todos))[0]
            return TodoResponse(
            error = None,
            todo=todo
           )
        except:
            return TodoResponse(
                error = f"todo of id {id} was not found.",
                todo=None
            )
schema = Schema(query=Query, mutation=Mutation)