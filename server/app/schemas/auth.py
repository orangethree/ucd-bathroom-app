from marshmallow import Schema, fields, validate


class LoginRequestSchema(Schema):
    google_id_token = fields.String(required=True)


class LoginResponseSchema(Schema):
    token = fields.String()
    user = fields.Dict()
