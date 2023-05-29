from concurrent import futures
import time
import grpc
from protos import hello_pb2_grpc, hello_pb2


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


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_HelloServicer_to_server(HelloServicer(), server)
    server.add_insecure_port("localhost:3001")
    server.start()
    print("The server has started....")
    server.wait_for_termination()


if __name__ == "__main__":
    run()
