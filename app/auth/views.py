from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token
from app.auth.models import User
from app import application


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route("/register", methods=["POST"])
def register():
    body = request.get_json()
    email = body["email"]
    user = User.objects(email=email)
    if user:
        return jsonify(message="User Already Exist"), 409
    else:
        User(**body).save()
        return jsonify(message="User added sucessfully"), 201


@auth.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    email = body["email"]
    user = User.objects(email=email).first()
    if user:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login Succeeded!", access_token=access_token), 201
    else:
        return jsonify(message="Bad Email or Password"), 401
        