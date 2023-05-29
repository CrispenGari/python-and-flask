from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DelayedReply(_message.Message):
    __slots__ = ["message", "request"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    message: str
    request: _containers.RepeatedCompositeFieldContainer[HelloRequest]
    def __init__(self, message: _Optional[str] = ..., request: _Optional[_Iterable[_Union[HelloRequest, _Mapping]]] = ...) -> None: ...

class HelloReply(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class HelloRequest(_message.Message):
    __slots__ = ["greeting", "name"]
    GREETING_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    greeting: str
    name: str
    def __init__(self, name: _Optional[str] = ..., greeting: _Optional[str] = ...) -> None: ...
