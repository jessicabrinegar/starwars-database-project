from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
# this is what is returned 
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String, unique=True, nullable=False)
    climate = db.Column(db.String(120), nullable=True)
    terrain = db.Column(db.String(120), nullable=True)

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String, unique=True, nullable=False)
    height = db.Column(db.String(120), nullable=True)
    haircolor = db.Column(db.String(120), nullable=True)