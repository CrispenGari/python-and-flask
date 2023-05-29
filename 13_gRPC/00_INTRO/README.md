### intro

In this one we are going to learn the basic concepts of `gRPC` using `python`. We are going to look at the following concepts in `grpc`:

- **Unary / Simple RPC**
- **Server Streaming**
- **Client Streaming**
- **Bidirectional Streaming**

First we need to initialize the project by creating a virtual environment and activate it as follows:

```shell
virtualenv venv && .\venv\Scripts\activate
```

Then we will need to install the following packages in our project.

```shell
pip install grpcio grpcio-tools
```

We can then create a `requirements.txt` file by running the following command:

```shell
pip freeze > requirements.txt
```

After that we are going to create a `server.py`, `client.py` and `protos/hello.proto` files in our root directory and in the `hello.proto` file we are going to add the following:

```proto
syntax = "proto3";

package hello;

// The hello service definition.
service Hello {
	// Unary
	rpc hello (HelloRequest) returns (HelloReply);

	// Server Streaming
	rpc parrotHello (HelloRequest) returns (stream HelloReply);

	// Client Streaming
	rpc clientHello (stream HelloRequest) returns (DelayedReply);

	// Both Streaming
	rpc biHello (stream HelloRequest) returns (stream HelloReply);
}

// The request message containing the user's name.
message HelloRequest {
  string name = 1;
  string greeting = 2;
}

// The response message containing the greetings.
message HelloReply {
  string message = 1;
}

message DelayedReply {
	string message = 1;
	repeated HelloRequest request = 2;
}

```

> You might need to install the following extensions if you are on `vscode`:

1. `Proto Lint`
2. `vscode-proto3`

### Unary Calls

Sometimes called a `simple RPC`. A simple RPC where the client sends a request to the server using the stub and waits for a response to come back, just like a normal function call.

Let's start by implementing our first `unary` call. This is where the client send the request to the server and get the response from the server.

Now that we have our `hello` package in the `proto/hello.proto` we can go ahead and run a command that will generate the gRPC code as follows:

```sh
 python -m grpc_tools.protoc -I./protos --python_out=./protos --pyi_out=./protos --grpc_python_out=./protos ./protos/*.proto
```

So with this command we are actually generating the `grpc` code from any file that we will find in the `protos` that has an extension `.proto` to the `proto` directory.

We are going to make our `protos` a package by creating a `__init__.py` and and the following code to it:

```py
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
```

The next thing is to create our `server.py` code.

```py
from concurrent import futures
import grpc
from protos import hello_pb2_grpc, hello_pb2

class HelloServicer(hello_pb2_grpc.HelloServicer):
    def hello(self, request, context):
        print(request)
        reply = hello_pb2.HelloReply(message=f"{request.greeting} {request.name}")
        return reply

def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_HelloServicer_to_server(HelloServicer(), server)
    server.add_insecure_port("localhost:3001")
    server.start()
    print("The server has started....")
    server.wait_for_termination()

if __name__ == "__main__":
    run()
```

You can now start the server by running the following command:

```shell
python server.py
```

In the `client.py` we are going to do pretty much the same thing.

```py
import grpc
from protos import hello_pb2_grpc, hello_pb2

def run():
    with grpc.insecure_channel("localhost:3001") as channel:
        stub = hello_pb2_grpc.HelloStub(channel)
        print("1. hello - Unary")
        print("2. parrotHello - Server Side Streaming")
        print("3. clientHello - Client Side Streaming")
        print("4. biHello - Bidirectional Streaming")
        call = int(input("Which rpc would you like to make: "))

        if call == 1:
            hello_request = hello_pb2.hello(greeting="Hello", name="World")
            hello_reply = stub.SayHello(hello_request)
            print(hello_reply)

if __name__ == "__main__":
    run()

```

When the server started you can now run the the following command to start the `client` on the other terminal:

```shell
python client.py
```

We will get the following logs on the client:

```shell
message: "Hello World
```

### Server Streaming

We have looked at unary calls, the next thing that we can have a look at is `server-side streaming`. A `server-side streaming` RPC where the client sends a request to the server and gets a stream to read a sequence of messages back.

Then in the `server.py` we are going to modify it to look as follows:

```py
class HelloServicer(hello_pb2_grpc.HelloServicer):
    def hello(self, request, context):
        print(request)
        reply = hello_pb2.HelloReply(message=f"{request.greeting} {request.name}")
        return reply

    def parrotHello(self, request, context):
        print(request)
        for i in range(3):
            hello_reply = hello_pb2.HelloReply(message=f"{request.greeting} {request.name} {i + 1}")
            yield hello_reply
            time.sleep(2)
```

In the client we are going to `modify` it to look as follows:

```py
def run():
    with grpc.insecure_channel("localhost:3001") as channel:
        stub = hello_pb2_grpc.HelloStub(channel)
        print("1. hello - Unary")
        print("2. parrotHello - Server Side Streaming")
        print("3. clientHello - Client Side Streaming")
        print("4. biHello - Bidirectional Streaming")
        call = int(input("Which rpc would you like to make: "))

        if call == 1:
            hello_request = hello_pb2.HelloRequest(greeting="Hello", name="World")
            hello_reply = stub.hello(hello_request)
            print(hello_reply)
        elif call == 2:
            hello_request = hello_pb2.HelloRequest(greeting="Hello", name="World")
            hello_replies = stub.parrotHello(hello_request)
            for hello_reply in hello_replies:
                print("*" * 20)
                print(hello_reply)
```

Now if you start the server and the client you will be able to get the following logs from the console.

```shell
********************
message: "Hello World 1"

********************
message: "Hello World 2"

********************
message: "Hello World 3"
```

We have succesifuly implemented the server-side streaming in `gRPC` next we are going to have a look at the `client-based` streaming.

### Client Streaming

A `client-side streaming` RPC where the client writes a sequence of messages and sends them to the server, again using a provided stream. Once the client has finished writing the messages, it waits for the server to read them all and return its response.

In our `server.py` we are going to add the following code in it:

```py
class HelloServicer(hello_pb2_grpc.HelloServicer):
    def hello(self, request, context):
        print(request)
        reply = hello_pb2.HelloReply(message=f"{request.greeting} {request.name}")
        return reply

    def parrotHello(self, request, context):
        print(request)
        for i in range(3):
            hello_reply = hello_pb2.HelloReply(
                message=f"{request.greeting} {request.name} {i + 1}"
            )
            yield hello_reply
            time.sleep(2)

    def clientHello(self, request_iterator, context):
        delayed_reply = hello_pb2.DelayedReply()
        for request in request_iterator:
            print("*" * 20)
            print(request)
            delayed_reply.request.append(request)
        delayed_reply.message = f"You have sent {len(delayed_reply.request)} messages. Please expect a delayed response."
        return delayed_reply

```

Then we will modify our `client.py` file to have the following code in it:

```py
def get_client_stream_requests():
    while True:
        name = input("Please enter a name (or nothing to stop chatting): ")
        if name == "":
            break
        hello_request = hello_pb2.HelloRequest(greeting="Hello", name=name)
        yield hello_request
        time.sleep(1)


def run():
    with grpc.insecure_channel("localhost:3001") as channel:
        stub = hello_pb2_grpc.HelloStub(channel)
        print("1. hello - Unary")
        print("2. parrotHello - Server Side Streaming")
        print("3. clientHello - Client Side Streaming")
        print("4. biHello - Bidirectional Streaming")
        call = int(input("Which rpc would you like to make: "))

        if call == 1:
            hello_request = hello_pb2.HelloRequest(greeting="Hello", name="World")
            hello_reply = stub.hello(hello_request)
            print(hello_reply)
        elif call == 2:
            hello_request = hello_pb2.HelloRequest(greeting="Hello", name="World")
            hello_replies = stub.parrotHello(hello_request)
            for hello_reply in hello_replies:
                print("*" * 20)
                print(hello_reply)
        elif call == 3:
            delayed_reply = stub.clientHello(get_client_stream_requests())
            print("*" * 20)
            print(delayed_reply)
```

Now if we start both our client and server we should see the following on the server console.

```shell
********************
name: "hello"
greeting: "Hello"

********************
name: "how are you"
greeting: "Hello"

********************
name: "i\'m fine"
greeting: "Hello"

********************
name: "bye"
greeting: "Hello"
```

On the client you will get the following logs:

```shell
Please enter a name (or nothing to stop chatting): hello
Please enter a name (or nothing to stop chatting): how are you
Please enter a name (or nothing to stop chatting): i'm fine
Please enter a name (or nothing to stop chatting): bye
Please enter a name (or nothing to stop chatting):
********************
message: "You have sent 4 messages. Please expect a delayed response."
request {
  name: "hello"
  greeting: "Hello"
}
request {
  name: "how are you"
  greeting: "Hello"
}
request {
  name: "i\'m fine"
  greeting: "Hello"
}
request {
  name: "bye"
  greeting: "Hello"
}
```

### Bidirectional Streaming

A `bidirectional streaming` RPC where both sides send a sequence of messages using a read-write stream.

In our `server.py` we are going to add the following code in it:

```py
class HelloServicer(hello_pb2_grpc.HelloServicer):
    def hello(self, request, context):
        print(request)
        reply = hello_pb2.HelloReply(message=f"{request.greeting} {request.name}")
        return reply

    def parrotHello(self, request, context):
        print(request)
        for i in range(3):
            hello_reply = hello_pb2.HelloReply(
                message=f"{request.greeting} {request.name} {i + 1}"
            )
            yield hello_reply
            time.sleep(2)

    def clientHello(self, request_iterator, context):
        delayed_reply = hello_pb2.DelayedReply()
        for request in request_iterator:
            print("*" * 20)
            print(request)
            delayed_reply.request.append(request)
        delayed_reply.message = f"You have sent {len(delayed_reply.request)} messages. Please expect a delayed response."
        return delayed_reply

    def biHello(self, request_iterator, context):
        for request in request_iterator:
            print("*" * 20)
            print(request)
            hello_reply = hello_pb2.HelloReply(
                message=f"{request.greeting} {request.name}"
            )
            yield hello_reply

```

Then we will modify our `client.py` file to have the following code in it:

```py
def get_client_stream_requests():
    while True:
        name = input("Please enter a name (or nothing to stop chatting): ")
        if name == "":
            break
        hello_request = hello_pb2.HelloRequest(greeting="Hello", name=name)
        yield hello_request
        time.sleep(1)


def run():
    with grpc.insecure_channel("localhost:3001") as channel:
        stub = hello_pb2_grpc.HelloStub(channel)
        print("1. hello - Unary")
        print("2. parrotHello - Server Side Streaming")
        print("3. clientHello - Client Side Streaming")
        print("4. biHello - Bidirectional Streaming")
        call = int(input("Which rpc would you like to make: "))

        if call == 1:
            hello_request = hello_pb2.HelloRequest(greeting="Hello", name="World")
            hello_reply = stub.hello(hello_request)
            print(hello_reply)
        elif call == 2:
            hello_request = hello_pb2.HelloRequest(greeting="Hello", name="World")
            hello_replies = stub.parrotHello(hello_request)
            for hello_reply in hello_replies:
                print("*" * 20)
                print(hello_reply)
        elif call == 3:
            delayed_reply = stub.clientHello(get_client_stream_requests())
            print("*" * 20)
            print(delayed_reply)
        elif call == 4:
            responses = stub.biHello(get_client_stream_requests())
            for response in responses:
                print("*" * 20)
                print(response)

```

Now on the server console you will see the following logs:

```shell
********************
name: "hello"
greeting: "Hello"

********************
name: "hi"
greeting: "Hello"
```

If the client is sending this:

```shell
Please enter a name (or nothing to stop chatting): hello
********************
message: "Hello hello"

Please enter a name (or nothing to stop chatting): hi
********************
message: "Hello hi"

```

### Refs

0. [python](https://grpc.io/docs/languages/python/quickstart/)
