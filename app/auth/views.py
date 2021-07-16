from app import application, db
from app.auth.serializers import UserLoginSchema, UserRegisterSchema
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError


auth = Blueprint('auth', __name__, url_prefix='/auth')


def _validate_request(schema, data):
    data = data.copy()
    try:
        schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400


@auth.route("/register", methods=["POST"])
def register():
    request_data = request.get_json()
    schema = UserRegisterSchema()
    _validate_request(schema, request_data)
    email = request_data["email"]
    user = db.users.find_one({"email": email})
    if user:
        return jsonify(message="User Already Exist"), 409
    else:
        db.users.insert_one(**request_data)
        return jsonify(message="User added sucessfully"), 201


@auth.route("/login", methods=["POST"])
def login():
    request_data = request.get_json()
    schema = UserLoginSchema()
    _validate_request(schema, request_data)
    email = request_data["email"]
    password = request_data["password"]
    user = db.users.find_one({"email": email, "password": password})
    if user:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login Succeeded!", access_token=access_token), 201
    else:
        return jsonify(message="Bad Email or Password"), 401