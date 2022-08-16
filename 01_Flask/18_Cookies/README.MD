### Cookies

Cookies are small files that websites send to your device that the sites then use to monitor you and remember certain information about you.

### Setting cookies from the Sever.

We are going to have an `html` file that we will render to the DOM and send cookies to it from the server. We are going to do it as follows:

```py
from flask import Flask, render_template
from flask.helpers import make_response
app = Flask(__name__)
app.config["ENV"] = "development"

@app.route('/cookies')
def home():
    res = make_response(render_template("index.html"))
    res.set_cookie("username", "root")
    return res

if __name__ == "__main__":
    app.run(debug=True)
```

So now if we visit http://127.0.0.1:5000/cookies and `inspect` the page and type:

```
> document.cookie
> "username=root"
```

We will see the cookie that we have set in the browser.

1. `set_cookie`
   This method allows us to send cookies to the browser from the flask server. It takes a lot of parameters:

```py
set_cookie(
    key,
    value='',
    max_age=None,
    expires=None,
    path='/',
    domain=None,
    secure=False,
    httponly=False,
    samesite=None
)
```

   <table>
      <thead>
        <tr>
          <th>Parameter</th>
          <th>Default</th>
          <th>Required</th>
          <td>Explanation</td>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>key</td>
          <td>(required)</td>
          <td>True</td>
          <td>Name of the cookie</td>
        </tr>
        <tr>
          <td>value</td>
          <td>""</td>
          <td>False</td>
          <td>value of the cookie</td>
        </tr>
        <tr>
          <td>max_age</td>
          <td>None</td>
          <td>False</td>
          <td>The age of a cookie in seconds</td>
        </tr>
        <tr>
          <td>expires</td>
          <td>None</td>
          <td>False</td>
          <td>The date of then the cookie expires, must be a datetime object</td>
        </tr>
        <tr>
          <td>path</td>
          <td>None</td>
          <td>False</td>
          <td>Limits the cookie to a given path</td>
        </tr>
        <tr>
          <td>domain</td>
          <td>None</td>
          <td>False</td>
          <td>specify a domain able to read the cookie (default is the domain that set it)</td>
        </tr>
        <tr>
          <td>secure</td>
          <td>False</td>
          <td>False</td>
          <td>If True, the cookie will only be available over HTTPS</td>
        </tr>
        <tr>
          <td>httponly</td>
          <td>False</td>
          <td>False</td>
          <td>Disallow JavaScript to access the cookie (Limited browser support)</td>
        </tr>
        <tr>
          <td>samesite</td>
          <td>False</td>
          <td>False</td>
          <td>Limits the scope of where the cookie is accessible to the same site</td>
        </tr>
      </tbody>
    </table>

### Accessing cookies

To get all the cookies we just call the `request.cookies` which will returns all the cookies inform of an `ImutableDict` of the browser for both the client and the server. Example:

```python
from flask import Flask, render_template
from flask.globals import request
from flask.helpers import make_response

app = Flask(__name__)
app.config["ENV"] = "development"

@app.route('/cookies')
def home():
    res = make_response(render_template("index.html"))
    res.set_cookie("username", "root")
    cookies = request.cookies
    print(cookies)
    return res

if __name__ == "__main__":
    app.run(debug=True)
```

### Setting cookies from the client.

Note that we can even set cookies from the client in javascript by doing the following:

```js
document.cookie = "key=value";
```
