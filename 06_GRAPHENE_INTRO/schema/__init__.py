
from graphene import ObjectType,  Schema
import graphene


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
class Mutation(ObjectType):
    create_todo = CreateTodo.Field(
        name="create_todo",
        description="creating todos"
    )
    delete_todo = DeleteTodo.Field()
    update_todo = UpdateTodo.Field()



class Query(ObjectType):
    todos = graphene.List(graphene.NonNull(Todo))
    todo = graphene.Field(TodoResponse, id=graphene.Int(required=True))

    hello = graphene.String()
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