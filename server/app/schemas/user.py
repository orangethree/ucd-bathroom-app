from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.String()
    username = fields.String()
    email = fields.String()
    trust_score = fields.Integer()
    created_at = fields.DateTime()
