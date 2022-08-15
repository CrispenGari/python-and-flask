
from app import app

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True, nullable=False)
    title = db.Column(db.String(80), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, title, completed):
        self.title = title
        self.completed = completed

    def __repr__(self):
        return '<Student %r>' % self.name
    
    def to_json(self):
        return {
            'title': self.title,
            'completed': self.completed,
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
# creating tables
db.create_all()