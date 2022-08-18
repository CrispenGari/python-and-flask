### Socket IO

In this practical we are going to create a socket-io server in python that allows client server sockect communication between the two. We are going to create a simple chat application using websockets.

### Installation

We are going to install all the packages that we are going to use by running the following command:

```shell
pip install flask-socketio flask
```

### Setup

We are going to create two folders which are:

1. `client` - contains a basic client application using `html`, `css` and `javascript`.
2. `server` - contains the server code.

### Sending and Receiving messages

In this section we are going to send and receive messages from the `client` to the `server`. We are going to write the server code in the `server/app.py` and the client code in the `client/index.js`. Note that in the client we are using a `CDN` from socketio that allows us to communicate with the server using websockets:

### on('message') || on('json')

These are the two unnamed events in `flask-socketio`

1. server code

```py
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdfghjkl'
io = SocketIO(app,  cors_allowed_origins='*')

@io.on('message')
def on_message(msg):
    print({'message': msg})

if __name__ == "__main__":
    io.run(app, '127.0.0.1', port=3001, debug=True)
```

2. client code

```js
const socket = io("http://127.0.0.1:3001");
socket.on("connect", () => {
  socket.emit("message", { data: "Connected to the server" });
});
```

> Now if we open the client app we will get the following print messages on the terminal.

```shell
{'message': {'data': 'Connected to the server'}}
```

### custom events.

Let's create our custom event called `user-connected` that allows us to send the user data from the client, when there's a new user connected.

1. server code

```py
@io.on('user-connected')
def on_user_connected(data):
    print({'data': data})
```

2. client code

```js
const socket = io("http://127.0.0.1:3001");
socket.on("connect", () => {
  socket.emit("user-connected", {
    id: socket.id,
    user: {
      username: "username",
      email: "email@gmail.com",
      id: 1,
    },
  });
});
```

> Now if we open the client app we will get the following print messages on the terminal.

```shell
{'data': {'id': 'kRGcpT24XHudf8XGAAAO', 'user': {'username': 'username', 'email': 'email@gmail.com', 'id': 1}}}
```

### namespaces.

> Flask-SocketIO also supports SocketIO namespaces, which allow the client to multiplex several independent connections on the same physical socket.

Let's create a namespace called `/user`

1. server code

```py
@io.on('user-connected', namespace='/user')
def on_user_connected(data):
    print({'data': data})
```

2. client code

```js
const socket = io("http://127.0.0.1:3001/user");
socket.on("connect", () => {
  //   socket.emit("my event", "Hello");
  socket.emit("user-connected", {
    id: socket.id,
    user: {
      username: "username",
      email: "email@gmail.com",
      id: 1,
    },
  });
});
```

> Now if we open the client app we will get the following print messages on the terminal.

```shell
{'data': {'id': 'jGFE52n-C6hGq7khAAAL', 'user': {'username': 'username', 'email': 'email@gmail.com', 'id': 1}}}
```

### sending message from the client.

Now that we have leant how to send the messages from the client, it's time for us to send the messages from the server to the client. For that we use the `send` or `emit` events.

> Note that the `send` is used for unnamed events and `emit` for named events.

1. server code

```py
@io.on('user-connected', namespace='/user')
def on_user_connected(data):
    print({'data': data})
    emit('new-user', data, callback= lambda: print('message was recieved'))

```

- the callback function will run if the message is successfully received by the client.

2. client code

```js
const socket = io("http://127.0.0.1:3001/user");
socket.on("connect", () => {
  //   socket.emit("my event", "Hello");
  socket.emit("user-connected", {
    id: socket.id,
    user: {
      username: "username",
      email: "email@gmail.com",
      id: 1,
    },
  });
  socket.on("new-user", (data) =>
    console.log({
      message: "new user is connected",
      data,
    })
  );
});
```

> Now we can send and receive the data from the server and client.

### broadcasting.

When a message is sent with the broadcast option enabled, all clients connected to the namespace receive it, including the sender.

1. server code

```py
@io.on('user-connected', namespace='/user')
def on_user_connected(data):
    print({'data': data})
    emit('new-user', data, broadcast=True)
```

> When broadcasting messages we just need to set the `broadcast` to `true` when we are emitting the message.

### Connection events

We can listen to the client connection events from our server using the `connect` and `disconnect` events.

1. server code

```py
@io.on('connect', namespace="/user")
def test_connect(auth):
    emit('my response', {'data': 'Connected'})

@io.on('disconnect', namespace='/user')
def test_disconnect():
    print('Client disconnected')
```

> The above listen to the connection and disconnection events of in a provided namespace.

### Rooms.

Socket io allows the concept of allowing users to join and leave the rooms using the `join_room` and `leave_room` functions.

1. server code

```py
@io.on('join-room')
def on_join(data):
    username = data['username']
    room = data['roomName']
    join_room(room)
    emit('new-user', {
        'message': username+ " Joined the room."
    }, broadcast=True, to=room)

@io.on('leave-room')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit(username + ' has left the room.', to=room)
```

2. client code

```js
document.querySelector("[join-btn]").addEventListener("click", () => {
  socket.emit("join-room", {
    id: socket.id,
    roomName: roomName.value,
    username: username.value,
  });
});
```

> Now if you click the join-room room button the user will be joined in that room.

### Simple chat app.

In this section we are to create a simple chat application.

1. `html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="index.css" />
    <script
      src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"
      integrity="sha512-q/dWJ3kcmjBLU4Qc47E4A9kTB4m3wuTY7vkFJDTZKjTs8jhyGQnaUrxa0Ytd0ssMZhbNua9hE+E7Qv1j+DyZwA=="
      crossorigin="anonymous"
    ></script>
    <title>Chat App</title>
  </head>
  <body>
    <div class="app">
      <ul id="messages"></ul>
      <input type="text" id="message" />
      <button id="sendbutton">Send</button>
    </div>
    <script src="index.js"></script>
  </body>
</html>
```

2. client - javascript

```js
const socket = io("http://127.0.0.1:3001/chat");
const messages = document.querySelector("#messages");
const message = document.querySelector("#message");
const sendBtn = document.getElementById("sendbutton");

socket.on("connect", function () {
  socket.send("User has connected!");
});

socket.on("new-message", function (msg) {
  const child = document.createElement("li");
  child.innerHTML = msg;
  messages.appendChild(child);
});

sendBtn.addEventListener("click", () => {
  socket.emit("message", message.value);
  message.value = "";
});
```

3. server

```py

from socket import socket
from flask import Flask
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdfghjkl'
io = SocketIO(app,  cors_allowed_origins='*')

@io.on('message', namespace='/chat')
def new_message(message):
    emit('new-message', message, broadcast=True)


if __name__ == "__main__":
    io.run(app, '127.0.0.1', port=3001, debug=True)
```

> Now we can be able to allow communication between one client and another using `socket.io`.

### Refs

1.[flask-socketio](https://flask-socketio.readthedocs.io/en/latest/getting_started.html)
