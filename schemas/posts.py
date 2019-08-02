from marshmallow import validate, Schema, fields
from schemas.comments import CommentSchema

class PostPointSchema(Schema):
    user_id = fields.Int(dump_only=True)
    post_id = fields.Int(dump_only=True)
    point_id = fields.Int(dump_only=True, autoincrement=True)
    points = fields.Int(validate=validate.Range(min=0, max=10))


class PostSchema(Schema):
    comments = fields.Nested(CommentSchema(), many=True)
    modified_at = fields.DateTime(dump_only=True)
    created_time = fields.DateTime(dump_only=True)
    user_id = fields.Int(required=True)
    post_text = fields.Str(required=True)
    post_id = fields.Int(dump_only=True)
    points = fields.Nested(PostPointSchema(), many=True)