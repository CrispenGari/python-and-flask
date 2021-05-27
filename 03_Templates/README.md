### Templates

Suppose we have the following list of dictioneries and we want to render it on the screen. We can use what we call the `template` syntax.

```python
workers =[
    {"id": 1, "name":"Worker1", "salary":1237.99},
    {"id": 2, "name":"Worker2", "salary":5237.99},
    {"id": 3, "name":"Worker5", "salary":5237.39}
]
```

We can do it as follows:

> `main.py`

```py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    workers =[
    {"id": 1, "name":"Worker1", "salary":1237.99},
    {"id": 2, "name":"Worker2", "salary":5237.99},
    {"id": 3, "name":"Worker5", "salary":5237.39}
    ]
    return render_template("html/home.html", workers=workers)

```

> `templates/html/home.html`.

```html
<body>
  <h1>All Workers</h1>
  {% for worker in workers%}
  <p>
    <span>{{worker.id}}</span><span>{{worker.name | upper}}</span
    ><span>{{worker.salary}}</span>
  </p>
  {% endfor%}
</body>
```

Displaying workers that has `id` greater than 1.

```html
<body>
  <h1>All Workers</h1>
  {% for worker in workers%} {% if worker.id > 1%}
  <p>
    <span>{{worker.id}}</span><span>{{worker.name | upper}}</span
    ><span>{{worker.salary}}</span>
  </p>
  {% endif %} {% endfor%}
</body>
```

### Templates inheritence.

Suppose we have webapp that has multiple pages with the same header. This means we can create a `base.html` file that all the pages can inherit from. Let's go ahead and implement two pages, the home page and the about page, and both of these should inherit from `base.html`.

File structures.

```
main.py
    templates
        -base.html
        html
            -home.html
            -about.html
```

> `base.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %} {% endblock %}</title>
  </head>
  <nav><a href="/">Home</a><a href="/about">About</a></nav>
  <body>
    {%block content%} {%endblock%}
  </body>
</html>
```

- `{% block title %}` this is where the title of block for each page will be rendered.
- `{%block content%}` in this region the content of each page will be rendered in here.

> `home.html`

```html
{% extends 'base.html' %} {%block title%} Home {%endblock%} {%block content%}
<h1>Home</h1>
{%endblock%}
```

- `{% extends 'base.html' %}` we are inheriting from the `base.html`
  > `about.html`

```html
{% extends 'base.html' %} {%block title%} About {%endblock%} {%block content%}
<h1>About</h1>
{%endblock%}
```

> `main.py`

```python
from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def home():
    workers =[
    {"id": 1, "name":"Worker1", "salary":1237.99},
    {"id": 2, "name":"Worker2", "salary":5237.99},
    {"id": 3, "name":"Worker5", "salary":5237.39}
    ]
    return render_template("html/home.html", workers=workers)

@app.route('/about', methods=["GET", "POST"])
def about():
    return render_template('html/about.html')
```
