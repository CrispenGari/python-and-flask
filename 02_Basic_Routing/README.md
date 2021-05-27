## Basic Routing

We use the `route()` decorator to bind a function to a URL.
Let's say we have 3 pages which are:

- home page
- about page
- profile page

To create the routes for these different pages the code is as follows:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home_page():
    return "<h1>Home Page</h1>"

@app.route('/about')
def about_page():
    return "<h1>About Page</h1>"

@app.route('/profile/<username>')
def profile_page(username):
    return f"<h1>About Page {username}</h1>"
```

### Variable Rules

I've already used the `variable rules` from the previous example in the `profile_page`.
You can add variable sections to a URL by marking sections with <variable_name>. Your function then receives the <variable_name> as a keyword argument. Optionally, you can use a converter to specify the type of the argument like <converter:variable_name>.

> The following `profile_page` will have a variable name with a `converter`:

```python
@app.route('/profile/<string:username>')
def profile_page(username):
    return f"<h1>About Page {username}</h1>"
```

### Converter types:

<table>
<thead>
<tr>
<th>Converter</th> <th>Explanation</th>
</tr>
</thead>
<tbody>
<tr>
<td>string</td><td>(default) accepts any text without a slash</td>
</tr>
<td>int</td><td>accepts positive integers</td>
</tr>
<td>float</td><td>accepts positive floating point values</td>
</tr>
<td>path</td><td>like string but also accepts slashes</td>
</tr>
<td>uuid</td><td>accepts UUID strings</td>
</tr>
</tbody>
</table>

### HTTP Methods.

There are two main `http` methods which are:

- GET
- POST

You can use the methods argument of the `route()` decorator to handle different HTTP methods. Example:

```python
from flask import request

@app.route('/about', methods=["GET", "POST"])
def about_page():
    if request.method == "GET":
        # do something
    else:
        # do something

    return "<h1>About Page</h1>"
```

### Rendering Templates

To render a template you can use the `render_template()` method. All you have to do is provide the name of the template and the variables you want to pass to the template engine as keyword arguments. Example:

First your files must look as follows:

```
main.py-
    -templates
        - home.html
        - about.html
        - profile.html
        ..
    - static
        - home.js
        - home.css
        - about.js
        ...
```

> `home.html`

```html
<body>
  <h1>Home</h1>
  {{ data }}
  <!--[0, 1.., 4]-->
</body>
```

> `app.py`

```py
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home_page():
    data =[
      i for i in range(5)
    ]
    return render_template("home.html", data=data)
```

### Displaying a list of numbers:

Just like `Django` the flask uses the `jinja` synthax to render html content.

```html
{% for number in data %}
<h1>{{number % 2}}</h1>
{% endfor%}

<!--Even Numbers-->
<h1>Even Numbers</h1>
{% for number in data %} {% if number%2 == 0 %}
<h1>{{ number}}</h1>
{% endif %} {% endfor%}
```
