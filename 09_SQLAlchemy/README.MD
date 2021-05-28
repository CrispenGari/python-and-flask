### SQLAlchemy

- Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application. It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.

* [Docs](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

### Installation

```shell
pip install -U Flask-SQLAlchemy
```

In this one we will have a system that will add students to the database and display them on the screen.

> `index.html`

```html
<center>
  <h1>Students</h1>
  {% with messages = get_flashed_messages()%} {% if messages %} {%for message in
  messages%}
  <li>{{message}}</li>
  {% endfor %} {% endif %} {% endwith%}
  <form action="#" method="post">
    <h1>Add Students</h1>
    <table>
      <tbody>
        <tr>
          <td>Name:</td>
          <td>
            <input type="text" name="name" placeholder="Enter Name" />
          </td>
        </tr>
        <tr>
          <td>Surname:</td>
          <td>
            <input type="text" name="surname" placeholder="Enter Surname" />
          </td>
        </tr>
        <tr>
          <td>Email:</td>
          <td>
            <input type="email" name="email" placeholder="Enter Email" />
          </td>
        </tr>
        <tr>
          <td>Gender:</td>
          <td>
            <input type="text" name="gender" placeholder="Enter Gender" />
          </td>
        </tr>
      </tbody>
    </table>
    <button type="submit">Add</button>
  </form>

  <h1>Students</h1>
  <table border="1">
    <thead>
      <tr>
        <th>Id</th>
        <th>Name</th>
        <th>Surname</th>
        <th>Email</th>
        <th>Gender</th>
      </tr>
    </thead>
    <tbody>
      {%for student in students%}
      <tr>
        <td>{{student.id}}</td>
        <td>{{student.name}}</td>
        <td>{{student.surname}}</td>
        <td>{{student.email}}</td>
        <td>{{student.gender}}</td>
      </tr>
      {%endfor%}
    </tbody>
  </table>
</center>
```

> `main.py`

```python
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "abcd"
"""
If SQLALCHEMY_DATABASE_URI is a relative path then we should use 3 slashes
for the uri otherwise 4 slashes.
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=7)

db = SQLAlchemy(app)
class Students(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120),  nullable=False)
    gender = db.Column(db.String(20),  nullable=False)
    surname = db.Column(db.String(120),  nullable=False)

    def __init__(self, name, email, gender, surname):
        self.name = name
        self.surname = surname
        self.email = email
        self.gender = gender

    def __repr__(self):
        return '<Student %r>' % self.name

"""
Make sure that you call the db.create_all() so that a table will be created.
"""
db.create_all()
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        gender = request.form["gender"]

        found_user = Students.query.filter_by(name=name).first()
        """
        We don't want to add students with the same name.
        """
        if found_user:
            flash("You can not add students with the same name.", "info")
        else:
            student = Students(name, email, gender, surname)
            db.session.add(student)
            db.session.commit()
            flash(f"{name} was added to our database.")
    students =Students.query.all()
    return render_template('index.html', students=students)
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True) # allow hot reloading

```

> Deleting, updating and linking the table can be found in the [Docs](https://flask-sqlalchemy.palletsprojects.com/en/2.x/).
