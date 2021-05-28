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