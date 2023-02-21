from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email
# this is what is returned 
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String, unique=True, nullable=False)
    climate = db.Column(db.String(120), nullable=True)
    terrain = db.Column(db.String(120), nullable=True)
    def serialize(self):
        return {
            "id": self.id,
            "planet_name": self.planet_name,
            "climate":self.climate,
            "terrain":self.terrain
        }

class Person(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String, unique=True, nullable=False)
    height = db.Column(db.String(120), nullable=True)
    haircolor = db.Column(db.String(120), nullable=True)
    def serialize(self):
        return {
            "id": self.id,
            "character_name": self.character_name,
            "height":self.height,
            "haircolor":self.haircolor
        }

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "person_id":self.person_id,
            "user_id":self.user_id
        }