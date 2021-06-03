### Query Strings

A query string is a part of a uniform resource locator (URL) that assigns values to specified parameters.

Consider the following url

```
https://google.com/search?name=ronaldo&like=football+wife
```

The URL is broken down into following peaces:

```
https ->  protocol
www.google.com ->  domain
/search -> path
?name=ronaldo&like=football+wife -> query strings
```

### Anatomy of a query string

```
? -> starts the query string
name -> is the first parameter
= ->  separates/assigns a value to the parameter
football+wife -> is the value assigned to the like parameter
```

### Getting the query string in flask.

To get the query string we use the `request.query_string` in flask.

```python

from flask import Flask, request
app = Flask(__name__)
app.config["ENV"] = "development"

@app.route('/home')

def home():
    if request.query_string:
        print(request.query_string)
    else:
        print ("No Query String")
    return "Home", 200
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading
```

If we go to this url http://localhost:5000/home?name=ronaldo&likes=football+wife. We get the following output to the console

```
b'name=ronaldo&likes=football+wife'
```

### Serializing query strings

To work with any kind of request object or data, we need to import request from flask:

```python

from flask import Flask, request
app = Flask(__name__)
app.config["ENV"] = "development"

@app.route('/home')

def home():
    if request.query_string:
        print(request.args)
    else:
        print ("No Query String")
    return "Home", 200
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading

```

If we go to the following url http://localhost:5000/home?name=ronaldo&likes=football+wife. We get the following output to the console.

```
ImmutableMultiDict([('name', 'ronaldo'), ('likes', 'football wife')])
```

- ImmutableMultiDict is just a special dict where values are accessed using the 'key' they works exactly the same as python `dict`.
