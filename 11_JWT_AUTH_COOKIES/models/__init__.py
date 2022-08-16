from app import db

class User(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120),  nullable=False, unique=True)
    password = db.Column(db.String(500),  nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
     
    def __init__(self, username, email,  password):
        self.username = username
        self.password = password
        self.email = email
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'updated_at': self.updated_at,
            'created_at': self.created_at,
        }
        
    
    
# create the tables

db.create_all()