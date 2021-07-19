from bson.objectid import ObjectId

import logging

from app import db
from app.game.constants import GameStatus
from app.game.game import Game
from app.game.serializers import GameMoveSchema, GameSchema, GameStartSchema
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

game = Blueprint("game", __name__, url_prefix="/games")

logger = logging.getLogger(__name__)


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
                "line_len_to_win": request_data["line_len_to_win"],
                "status": GameStatus.IN_PROGRESS,
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


@game.route("/<string:game_id>/move", methods=["POST"])
@jwt_required()
def move(game_id):
    current_user = get_jwt_identity()
    mongo_game = db.games.find_one_or_404(
        {"_id": ObjectId(game_id), "user": current_user}
    )
    status = mongo_game["status"]
    if not status == GameStatus.IN_PROGRESS:
        return jsonify(message=f"Game has ended with status: {status}"), 400

    request_data = request.get_json()
    try:
        GameMoveSchema().load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    u_x, u_y = request_data["x"], request_data["y"]
    game = Game.from_mongo(mongo_game)
    free_cells = game.free_cells

    if (u_x, u_y) not in free_cells:
        return (
            jsonify(f"You can't move at this cell. Free board cells are: {free_cells}"),
            400,
        )

    game.make_move((u_x, u_y), computer=False)
    user_move, computer_move = (u_x, u_y), None

    if game.has_won(computer=False) or not game.free_cells:
        pass
    else:
        c_x, x_y = game.calculate_move()
        game.make_move((c_x, x_y), computer=True)
        computer_move = (c_x, x_y)
    data = game.data_for_mongo
    logger.error(f"!!!!! Data for mongo: {data}")
    db.games.find_one_and_update({"_id": ObjectId(game_id)}, {"$set": data})
    return jsonify(
        your_move=user_move, computer_move=computer_move, game_status=data["status"]
    )
