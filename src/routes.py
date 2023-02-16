
"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from models import db, User, People, Planet, Favorite
from utils import generate_sitemap, APIException
# import bcrypt
# from flask_jwt_extended import create_access_token, jwt_required

api = Blueprint('api', __name__)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200


# create a new planet
@api.route('/planet', methods=['POST'])
def create_planet():
    rb = request.get_json()
    planet = Planet(planet_name=rb["planet_name"], climate=rb["climate"], terrain=rb["terrain"])
    db.session.add(planet)
    db.session.commit()
    return f"Planet {rb['planet_name']} was added", 200

# create a new person (character)
@api.route('/person', methods=['POST'])
def create_person():
    rb = request.get_json()
    person = Person(character_name=rb["character_name"], height=rb["height"], haircolor=rb["haircolor"])
    db.session.add(person)
    db.session.commit()
    return f"Character {rb['character_name']} was added", 200

# create a new favorite planet
@api.route('/favorite/planet/<int:id>', methods=['POST'])
def create_planet_favorite(user_id):
    rb = request.get_json()
    planet = Planet.query.get(id)
    if planet is None:
        raise APIException("Planet not found", 404)
    favorite = Favorite(planet_id=rb["planet_id"], user_id=user_id)
    db.session.add(favorite)
    db.session.commit()
    return f"Favorite planet was added", 200

# create a new favorite character
@api.route('/favorite/person/<int:id>', methods=['POST'])
def create_character_favorite(id, user_id):
    rb = request.get_json()
    person = Person.query.get(id)
    if person is None:
        raise APIException("Person not found", 404)
    favorite = Favorite(person_id=person.id, user_id=user_id)
    db.session.add(favorite)
    db.session.commit()
    return f"Favorite person was added", 200

# get list of all users
@api.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_list = list(map(lambda user: user.serialize(), users))
    return jsonify(users_list), 200

# get list of all planets
@api.route('/planet', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    planets_list = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets_list), 200

# get all the favorites that belong to a current user
@api.route('/users/favorites', methods=['GET'])
def get_user_favorites(user_id):
    favorites = Favorite.query.all(user_id)
    favorites_list = list(map(lambda favorite: favorite.serialize(), favorites))
    return jsonify(favorites_list), 200

# get a planet
@api.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):
    # put in the primary key as argument to get
    planet = Planet.query.get(id)
    if planet is None:
        raise APIException("Planet not found", 404)
    return jsonify(planet.serialize()), 200

# get a character
@api.route('/person/<int:id>', methods=['GET'])
def get_planet(id):
    # put in the primary key as argument to get
    person = Person.query.get(id)
    if planet is None:
        raise APIException("Planet not found", 404)
    return jsonify(planet.serialize()), 200

# update a planet
@api.route('/planet/<int:id>', methods=['PUT'])
def update_planet(id):
    planet = Planet.query.get(id)
    if planet is None:
        raise APIException("Planet not found", 404)
    rb = request.get_json()
    if "planet_name" in rb:
        planet.planet_name = rb["planet_name"]
    if "climate" in rb:
        planet.climate = rb["climate"]
    if "terrain" in rb:
        planet.terrain = rb["terrain"]
    db.session.commit()
    return jsonify(planet.serialize()), 200

# delete a planet
@api.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet():
    rb = request.get_json()
    planet = Planet(planet_name=rb["planet_name"])
    db.session.delete(planet)
    db.session.commit()
    return f"Planet {rb['planet_name']} was deleted", 200

# delete favorite character
@api.route('/favorite/person/<int:id>', methods=['DELETE'])
def delete_character_favorite(user_id):
    rb = request.get_json()
    favorite = Favorite(person_id=rb["person_id"], user_id=user_id)
    if favorite is None:
        raise APIException("Favorite not found", 404)
    db.session.delete(favorite)
    db.session.commit()
    return f"Favorite person was deleted", 200

# delete favorite planet
@api.route('/favorite/planet/<int:id>', methods=['DELETE'])
def delete_planet_favorite(user_id):
    rb = request.get_json()
    favorite = Favorite(planet_id=rb["planet_id"], user_id=user_id)
    if favorite is None:
        raise APIException("Favorite not found", 404)
    db.session.delete(favorite)
    db.session.commit()
    return f"Favorite planet was deleted", 200

# registration route for a user -- send post request to create new instance of class User to save to database
# send back the JWT in response
# @api.route('/register', methods=['POST'])
# def create_user():
    # request body
    # rb = request.get_json()
    # new_user = User(
    #     email=rb["email"], 
        # need to hash the password!
        # password=bcrypt.hashpw(rb["password"].encode('utf-8'), bcrypt.gensalt()), 
        # is_active=True
        # )
    # db.session.add(new_user)
    # db.session.commit()
    # access_token = create_access_token(identity=new_user.email)
    # return access_token, 200

#@api.route('/restricted', methods=['GET'])
# to make a restricted route, apply the following decorator: 
#@jwt_required
# def get_restricted():