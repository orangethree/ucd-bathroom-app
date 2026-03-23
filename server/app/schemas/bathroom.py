from marshmallow import Schema, fields


class BathroomSchema(Schema):
    id = fields.String()
    building_name = fields.String()
    floor_level = fields.String()
    latitude = fields.Float()
    longitude = fields.Float()
    gender_type = fields.String()
    is_accessible = fields.Boolean()
    created_at = fields.DateTime()


class BathroomDetailSchema(BathroomSchema):
    avg_overall_rating = fields.Float(allow_none=True)
    avg_cleanliness = fields.Float(allow_none=True)
    review_count = fields.Integer()
