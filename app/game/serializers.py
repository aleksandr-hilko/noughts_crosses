import datetime
from venv import create

from marshmallow import Schema, ValidationError, fields, validate, validates_schema


class GameStartSchema(Schema):
    board_size = fields.Integer(validate=validate.Range(min=3, max=10), required=True)
    line_len_to_win = fields.Integer(required=True)

    @validates_schema
    def validate_line_len(self, data, **kwargs):
        if data["line_len_to_win"] > data["board_size"]:
            raise ValidationError(
                "Length of sequence to win the game can't be greater than board size."
            )


class GameMoveSchema(Schema):
    order = fields.Int()
    coords = fields.Tuple((fields.Int, fields.Int))


class GameSchema(Schema):
    _id = fields.String()
    user = fields.Str()
    board_size = fields.Int()
    user_moves = fields.Nested(GameMoveSchema, many=True)
    computer_moves = fields.Nested(GameMoveSchema, many=True)
    line_len_to_win = fields.Int()
    status = fields.Str()
    created_at = fields.DateTime(missing=None, default=None)
    completed_at = fields.DateTime(missing=None, default=None)
    number_of_moves = fields.Method("get_number_of_moves")
    duration = fields.Method("get_duration")

    def get_number_of_moves(self, instance):
        return max(len(instance["user_moves"]), len(instance["computer_moves"]))

    def get_duration(self, instance):
        created_at, completed_at = instance.get("created_at"), instance.get(
            "completed_at"
        )
        if created_at and completed_at:
            duration = completed_at - created_at
        else:
            duration = datetime.datetime.now() - created_at
        return str(duration)


class GameMoveSchema(Schema):
    x = fields.Int()
    y = fields.Int()
