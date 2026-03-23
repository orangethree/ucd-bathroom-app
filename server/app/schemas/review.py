from marshmallow import Schema, fields, validate


class ReviewSchema(Schema):
    id = fields.String(dump_only=True)
    user_id = fields.String(dump_only=True)
    bathroom_id = fields.String(dump_only=True)
    overall_rating = fields.Integer(
        required=True, validate=validate.Range(min=1, max=5)
    )
    cleanliness = fields.Integer(
        required=True, validate=validate.Range(min=1, max=5)
    )
    traffic_level = fields.String(
        required=True,
        validate=validate.OneOf(['Empty', 'Low', 'Moderate', 'Busy', 'Packed']),
    )
    review_text = fields.String(load_default=None)
    created_at = fields.DateTime(dump_only=True)
    username = fields.String(dump_only=True)
