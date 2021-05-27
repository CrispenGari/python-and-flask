### Project layout.

The flask project file layout should look as follows which is known as good practice,

```python
project
        ├── application/
        │   ├── __init__.py
        │   ├── db.py
        │   ├── schema.sql
        │   ├── auth.py
        │   ├── blog.py
        │   ├── templates/
        │   │   ├── base.html
        │   │   ├── auth/
        │   │   │   ├── login.html
        │   │   │   └── register.html
        │   │   └── blog/
        │   │       ├── create.html
        │   │       ├── index.html
        │   │       └── update.html
        │   └── static/
        │       └── style.css
        ├── tests/
        │   ├── conftest.py
        │   ├── data.sql
        │   ├── test_factory.py
        │   ├── test_db.py
        │   ├── test_auth.py
        │   └── test_blog.py
        ├── venv/
        ├── setup.py
        └── MANIFEST.in
```

_Taken from [Flask](https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/)_.
