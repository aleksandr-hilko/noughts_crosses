from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class GameStartSchema(Schema):
    board_size = fields.Integer(validate=validate.Range(min=3, max=10), required=True)
    line_len_to_win = fields.Integer(required=True)

    @validates_schema   
    def validate_line_len(self, data, **kwargs):
        if data["line_len_to_win"] > data["board_size"]:
            raise ValidationError("Length of sequence to win the game can't be greater than board size.")


class GameSchema(Schema):
    _id = fields.String()
    user = fields.Str()
    board_size = fields.Int()
    user_moves = fields.List(fields.Tuple((fields.Int, fields.Int)))
    computer_moves = fields.List(fields.Tuple((fields.Int, fields.Int)))
    line_len_to_win = fields.Int()
    status = fields.Str()


class GameMoveSchema(Schema):
    x = fields.Int()
    y = fields.Int()
