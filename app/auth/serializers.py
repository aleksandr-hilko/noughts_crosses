from marshmallow import Schema, fields, ValidationError

class UserRegisterSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
