from api import db
class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    profileId = db.Column(db.String(50), nullable=False, unique=True)
    gender = db.Column(db.String(15), nullable=False)
    userId = db.Column(db.String(50), db.ForeignKey('user.userId'),
        nullable=False)

    def __repr__(self) -> str:
        return '<Profile %r>' % self.profileId

    def to_dict(self):
         return {
            "userId": str(self.userId),
            "profileId": self.profileId,
            "gender": self.gender
        }

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    userId = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    profile = db.relationship('Profile', backref='profile', lazy=True, uselist=False)
        
    def __repr__(self) -> str:
        return '<User %r>' % self.username

    def to_dict(self):
         return {
            "userId": str(self.userId),
            "username": self.username,
            "profile": self.profile
        }

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    addresses = db.relationship('Address', backref='person', lazy=True, cascade="all, delete")

    def __repr__(self) -> str:
        return '<Person %r>' % self.name

    def to_dict(self):
         return {
            "id": str(self.id),
            "name": self.name,
            "addresses": self.addresses.to_dict()
        }

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)

    def __repr__(self) -> str:
        return '<Address %r>' % self.email

    def to_dict(self):
         return {
            "id": str(self.id),
            "email": self.email,
            "person_id": self.person_id
        }

questions_categories = db.Table('questions_categories',
    db.Column('question_id', db.Integer, 
    db.ForeignKey('question.id'), primary_key=True),
    db.Column('category_id', db.Integer,
     db.ForeignKey('category.id'), primary_key=True)
)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(25), nullable=False)
    categories = db.relationship('Category', secondary=questions_categories, lazy='subquery',
        backref=db.backref('questions', lazy=True))

    def __repr__(self) -> str:
        return '<Question %r>' % self.question

    def to_dict(self):
         return {
            "id": self.id,
            "question": self.question,
            "categories": self.categories
        }
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(25), nullable=False)

    def __repr__(self) -> str:
        return '<Category %r>' % self.category

    def to_dict(self):
         return {
            "id": self.id,
            "category": self.category,
        }



