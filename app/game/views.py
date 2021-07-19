import datetime
import logging
import random

from bson.objectid import ObjectId

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
    """
    post: Endpoint that should be called to start a game.
    User should pass board_size and line_len_to_win, which
    is a number of points in a line whihc is used
    as a condition to win.
    """
    request_data = request.get_json()
    schema = GameStartSchema()
    try:
        schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    else:
        current_user = get_jwt_identity()
        computer_first = random.choice([True, False])
        game = db.games.insert_one(
            {
                "user": current_user,
                "board_size": request_data["board_size"],
                "user_moves": [],
                "computer_moves": [],
                "completed": False,
                "line_len_to_win": request_data["line_len_to_win"],
                "status": GameStatus.IN_PROGRESS,
                "created_at": datetime.datetime.now(),
                "computer_first": computer_first,
            }
        )
    return jsonify(message="Game has started", game_id=str(_id.inserted_id)), 201


@game.route("/", methods=["GET"])
@jwt_required()
def games_list():
    """
    get: Get list on current games for user along with some statistics details.
    """
    current_user = get_jwt_identity()
    schema = GameSchema(many=True)
    games = db.games.find({"user": current_user})
    return jsonify(schema.dump(games))


@game.route("/<string:game_id>/move", methods=["POST"])
@jwt_required()
def move(game_id):
    """
    post: Main endpoint to play a game.
    User should pass desired coordinates to move on here
    on success should receive computer move alond with
    status of a game.
    Coordinates are validated within current board position.
    """
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
    u_coords = request_data["x"], request_data["y"]
    game = Game.from_mongo(mongo_game)
    free_cells = game.free_cells

    if u_coords not in free_cells:
        return (
            jsonify(f"You can't move at this cell. Free board cells are: {free_cells}"),
            400,
        )

    computer_first = mongo_game.get("computer_first", False)
    moves_order = (True, False) if computer_first else (False, True)
    c_coords = None
    for computer_move in moves_order:
        if computer_move:
            coords = game.calculate_move()
            c_coords = coords
        else:
            coords = u_coords
        game.make_move(coords, computer=computer_move)
        if game.has_won(computer=computer_move) or not game.free_cells:
            break
    data = game.data_for_mongo
    db.games.find_one_and_update({"_id": ObjectId(game_id)}, {"$set": data})
    return jsonify(
        your_move=u_coords, computer_move=c_coords, game_status=data["status"]
    )
