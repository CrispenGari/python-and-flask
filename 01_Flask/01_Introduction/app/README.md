### Introduction

### Basic Flask application

- Make sure to not call your `application` `flask.py` because this would conflict with Flask. itself.

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

```

To run the application, use the flask command or python -m flask. Before you can do that you need to tell your terminal the application to work with by exporting the FLASK_APP environment variable:

```cmd
$cd app
Then
$ set FLASK_APP=main

Then

$ flask run
```

### Debug mode.

This will allow us to `hot_reload` the saver when the code changes, so to enable it we run the following command:

```shell

$set FLASK_DEBUG=True
```
