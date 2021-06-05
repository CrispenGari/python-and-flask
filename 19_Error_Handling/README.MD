### Error Handling

Up to now we are using flask error handlers for example if we visit http://127.0.0.1:5000/cookies and that url is not available we get an error page from flask. How about we create our own page that will be displayed, for example if there's a `404` error we display our custom 404 page that is good looking.

But before we go there it is good to know that when we want to throw an error to the browser we use the `abort()` method from flask for example:

```py
abort(404)  # Not found
abort(405)  # Method Not allowed
abort(500)  # Internal Server Error
```

### Custom error handlers

Just as we can throw errors on demand, we can handle them using the `errorhandler()` decorator and attaching it to our app instance.

The syntax for a custom error handler:

```py
@app.errorhandler(STATUS_CODE)
def function_name(error):
    ......
    return render_template("handler.html"), STATUS_CODE
```

Example: Handling a 404 error on our page

```py
import os
from flask import Flask
import flask

app = Flask(__name__)
app.config["ENV"] = "development"

@app.errorhandler(404)
def error_404(e):
    print(e)
    status = 403 + 1
    return flask.render_template("error.html", status=status), status
if __name__ == "__main__":
    app.run(debug=True)
```

As intended we are getting our own custom page displaying the error.
