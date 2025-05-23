# schemas.py
from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=1))
    name     = fields.Str(required=True, validate=validate.Length(min=1))
    role     = fields.Str(required=True, validate=validate.OneOf(['student','tutor']))

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)