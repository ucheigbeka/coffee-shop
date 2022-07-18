from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.after_request
def update_headers(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


# Ensure that this section is uncommented when first running the server in other to create
# the database. Also, it should be uncommented when performing integration testing with
# Postman
#
# db_drop_and_create_all()

# ROUTES


@app.route('/drinks')
def get_drinks():
    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in Drink.query.all()]
    }), 200


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in Drink.query.all()]
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    try:
        drinks_json = request.get_json()
        new_drink = Drink(title=drinks_json['title'], recipe=json.dumps(drinks_json['recipe']))
        new_drink.insert()
    except KeyError:
        abort(400)
    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in Drink.query.all()]
    }), 200


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    drink_json = request.get_json()
    drink = Drink.query.get_or_404(drink_id)
    drink.title = drink_json.get('title', drink.title)
    drink.recipe = json.dumps(drink_json.get('recipe', json.loads(drink.recipe)))
    drink.update()
    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in Drink.query.all()]
    }), 200


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    Drink.query.get_or_404(drink_id).delete()
    return jsonify({
        'success': True,
        'delete': drink_id
    }), 200


# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(e: AuthError):
    return jsonify(e.error), e.status_code
