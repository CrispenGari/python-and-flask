### Blueprints.

A view function is the code you write to respond to requests to your application. Flask uses patterns to match the incoming request URL to the view that should handle it. The view returns data that Flask turns into an outgoing response. Flask can also go the other direction and generate a URL to a view based on its name and arguments.

- [Docs](https://flask.palletsprojects.com/en/1.1.x/tutorial/views/)

Firstly we have the following file structures:

```python
app-
    - static
    - templates
    - blueprint.py
    - main.py
```

We want ti create a blue print that will serve the `index.html`.

> `blueprint.py`

```python
from flask import Blueprint, render_template

blueprint = Blueprint("blueprint",__name__, static_folder="static", template_folder="templates")

@blueprint.route('/')
def home():
    return render_template('index.html')

@blueprint.route('/test')
def test():
    return "Test"
```

> `main.py`

```py
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash
from blueprint import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint, url_prefix="/users")

@app.route('/')
def home():
    return "Home"
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading
```

> `index.html`

```html
<body>
  <h1>Blue Prints</h1>
</body>
```

### So how does it work?

We have `/` route that is in the `main.py` and we also have another `/` route in the `blueprint.py` so, because in the `main.py` we have specified `url_prefix='users'` then which means we only render `index.html` if the route has `/users` as it's prefix. If we did not specify the prefix then by default flask will render the `index.html` file to the page.

### Organizing files

We want to change the python files to have the following structure:

```python
app-
    - users
        - static
        - templates
        - blueprint.py
    - __init__.py
    - main.py
```

Create a `__init__.py` file inside the `users` folder this will let python know that we are creating a package `users`. Do not write anything into it go ahead and change the `main.py` to:

> `main.py`

```python
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash
from users.blueprint import blueprint # changed this

app = Flask(__name__)
app.register_blueprint(blueprint, url_prefix="/users")

@app.route('/')
def home():
    return "Home"
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading
```

- This will work as before.

### Why blueprints?

- They helps us to organize our files
- allows us to be able to create our own templates.
