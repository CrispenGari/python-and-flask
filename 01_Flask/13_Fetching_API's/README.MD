### The JavaScript `fetch()` API.

In this notebook we want to create a simple application that will send the information to the server as well as getting information from the server.

The code in the files will look as follows:

> `main.py`

```python

from flask import Flask, render_template, request
from flask.helpers import make_response
from flask.json import jsonify

app = Flask(__name__)
app.config["ENV"] = "development"

users = [
    {
        "id": 1,
        "username": "user1",
        "message": "This is the message from user1."
    },
      {
          "id": 2,
        "username": "user2",
        "message": "This is the message from user2."
    },
      {
          "id": 3,
        "username": "user3",
        "message": "This is the message from user3."
    }
]
@app.route('/users', methods=["GET"])
def all_users():
    return make_response(jsonify(users), 200)

@app.route('/user', methods=["POST"])
def user():
    if request.method == "POST":
        if request.is_json:
            res = request.get_json()
            # Add to the users database
            print(res)
            return "Created", 201
    return "Error", 500

@app.route('/')
def home():
    return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading
```

This sever just render the client file `index.html`

- Open a connection on http://localhost:5000/users to send all the users to the client when the fetch api is called in a javascript file.
- Open a connection on http://localhost:5000/user to allow a user to be posted to the server using the javascript fetch api

> `index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="{{url_for('static', filename='index.css')}}" />
    <title>Users</title>
  </head>
  <body>
    <h1>Home</h1>
    <div class="app">
      <form class="app__form">
        <h1>Add User</h1>
        <input type="text" placeholder="id" id="id" />
        <input type="text" placeholder="username" id="username" />
        <input type="text" placeholder="message" id="message" />
        <button type="submit" id="btn">add</button>
      </form>
      <div class="app__users">
        <h1>Users</h1>
      </div>
    </div>
    <script src="{{url_for('static', filename='index.js')}}"></script>
  </body>
</html>
```

The template that will be rendered

> `index.js`

```js
const users = document.querySelector(".app__users");

(async () =>
  await fetch("http://localhost:5000/users", {
    method: "GET",
  })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      console.log(data);
      const all_users = data
        ?.map(
          (u) =>
            `<div class="app__user">
              <p><strong>@${u.username}: </strong>${u.message}</p>
            </div>`
        )
        .join("");
      users.innerHTML = all_users;
    }))();

document.getElementById("btn").addEventListener("click", (e) => {
  e.preventDefault();
  const id = document.getElementById("id").value;
  const username = document.getElementById("username").value;
  const message = document.getElementById("message").value;
  const user = {
    username: username,
    id: id,
    message: message,
  };
  (async () => {
    fetch(`http://localhost:5000/user`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(user),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json",
      }),
    })
      .then((res) => console.log(res))
      .catch((err) => {
        console.log(err);
      });
  })();
});
```

- The client side file where we request the infomation and post to the server

> `index.css`

```css
* {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  box-sizing: border-box;
}
body {
  background: #fafafa;
}
h1 {
  font-size: 16px;
  font-weight: 500;
  text-align: center;
  margin: 20px auto;
}
.app {
  width: 100%;
  height: 100vh;
}
.app__form,
.app__users {
  width: 100%;
  max-width: 500px;
  background-color: white;
  box-shadow: 2px 2px 2px 2px solid lightgray;
  border-radius: 5px;
  margin: 10px auto;
  padding: 10px;
  display: flex;
  flex-direction: column;
}
input {
  width: 90%;
  margin: 10px auto;
  border: 1px solid lightseagreen;
  outline: none;
  border-radius: 5px;
  padding: 5px;
}
button {
  background: black;
  color: white;
  width: 50%;
  margin: 20px auto;
  border: 1px solid blueviolet;
  cursor: pointer;
  padding: 5px;
  outline: none;
  border-radius: 5px;
}
.app__user {
  width: 100%;
  padding: 5px;
  background-color: #fafafa;
  margin: 10px 0;
}
.app__user:nth-child(odd) {
  background-color: white;
}
p {
  width: 100%;
  font-size: 16px;
  letter-spacing: 1px;
  border-radius: 5px;
}
```

- This file is for styling the page.
