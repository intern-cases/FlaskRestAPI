from marshmallow import fields, validate, Schema
from schemas.posts import PostSchema
from schemas.comments import CommentSchema


class UserPointSchema(Schema):
    user_id = fields.Int(dump_only=True)
    point_id = fields.Int(dump_only=True, autoincrement=True)
    points = fields.Int(validate=validate.Range(min=0, max=10))


class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    raw_password = fields.Str(required=True)
    created_time = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    posts = fields.Nested(PostSchema(), many=True)
    comments = fields.Nested(CommentSchema(), many=True)
    points = fields.Nested(UserPointSchema(), many=True)
