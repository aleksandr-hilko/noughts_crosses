from marshmallow import Schema, fields, validate


class GameStartSchema(Schema):
    board_size = fields.Integer(validate=validate.Range(min=3, max=10), required=True)


class GameSchema(Schema):
    user = fields.Str()
    board_size = fields.Int()
    user_moves = fields.List(fields.Int())
    computer_moves = fields.List(fields.Int())
