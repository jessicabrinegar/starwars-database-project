
"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from models import db, User, People, Planet
from utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200

@api.route('/planet', methods=['POST'])
def create_planet():
    rb = request.get_json()
    planet = Planet(planet_name=rb["planet_name"], climate=rb["climate"], terrain=rb["terrain"])
    db.session.add(planet)
    db.session.commit()
    return f"Planet {rb['planet_name']} was added", 200

@api.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):
    # put in the primary key as argument to get
    planet = Planet.query.get(id)
    if planet is None:
        raise APIException("Planet not found", 404)
    return jsonify(planet.serialize()), 200

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

@api.route('/planet', methods=['DELETE'])
def delete_planet():
    rb = request.get_json()
    planet = Planet(planet_name=rb["planet_name"], climate=rb["climate"], terrain=rb["terrain"])
    db.session.delete(planet)
    db.session.commit()
    return f"Planet {rb['planet_name']} was deleted", 200

@api.route('/planet', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    planets_list = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets_list), 200