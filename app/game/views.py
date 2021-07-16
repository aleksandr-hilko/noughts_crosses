from app import db
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.game.serializers import GameStartSchema, GameSchema


game = Blueprint('game', __name__, url_prefix='/games')


@game.route("/", methods=["POST"])
@jwt_required()
def start_game():
    request_data = request.get_json()
    schema = GameStartSchema()
    try:
        schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    else:
        current_user = get_jwt_identity()
        db.games.insert_one(
            {
                "user": current_user, 
                "board_size": request_data["board_size"], 
                "user_moves": [], 
                "computer_moves": [], 
                "completed": False,
            }
        )
    return jsonify(message="Game has started"), 201



@game.route("/", methods=["GET"])
@jwt_required()
def games_list():
    current_user = get_jwt_identity()
    schema = GameSchema(many=True)
    games = db.games.find({"user": current_user})
    return jsonify(schema.dump(games))


# @game.route('<>/move', methods=['POST'])
# def move():
#     post = request.get_json()
