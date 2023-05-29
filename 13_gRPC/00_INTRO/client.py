import time
import grpc
from protos import hello_pb2_grpc, hello_pb2


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


if __name__ == "__main__":
    run()
