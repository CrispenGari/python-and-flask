### Application Config

Every Flask application has a global config object which can be accessed via `app.config`.Flask's config object allows us to assign values to configuration variables, which we'll then have access to throughout our application. The global config object can be treated just like a Python dictionary, which we can access and modify using key and values.

### Let's print the `app.config` object.

```python

from flask import Flask

app = Flask(__name__)
app.config["ENV"] = "development"

print(app.config)

@app.route('/')
def home():
    return "Home"
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading

```

If we run `python main.py` we will be greeted with a huge Config object with keys and values. We can also set our config variable by just doing the following:

```python
app.config["DB_NAME"] = "users"
```

This means `users` as our database name is visible throughout our flask application

### App Configuration file

So called `Good Practice` I love it!!

Flask allows us to create a configuration file, where we can place all of our config values, overwrite the default values and create our own. There are a few option for this, however we're just going to cover our preferred method of creating a Python file and creating a Config class. Go ahead and create a new file called `config.py`.

> `config.py`

```py
class Config:
    DEBUG = False
    TESTING = False
    ENV = "production"

class Development(Config):
    DEBUG = True
    ENV = "development"

class Testing(Config):
    TESTING =True

class Production:
    pass
```

Now we have a very basic config file, for Testing, Development and Production environment. So how do we use this?

### Loading a config file.

Loading a config file is a simple one liner and should be placed as close to wherever you've created your app object. It's best practice to load the config as soon as possible, just after your app object is created so any other extension has access to your configuration variables.
We load a config file with the `from_object()` method, for example:

```py
app.config.from_object("config_filename.ConfigClass")
```

Now let's try to load our application Development config in the `main.py`

```python

from flask import Flask

app = Flask(__name__)
app.config.from_object("config.Production")
@app.route('/')
def home():
    return "Home"
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading
```
