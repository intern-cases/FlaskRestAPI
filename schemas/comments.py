from marshmallow import Schema, validate, fields


class CommentPointSchema(Schema):
    comment_id = fields.Int(dump_only=True)
    point_id = fields.Int(dump_only=True, autoincrement=True)
    points = fields.Int(validate=validate.Range(min=0, max=10))


class CommentSchema(Schema):
    comment_id = fields.Int(dump_only=True)
    comment_text = fields.Str(required=True)
    user_id = fields.Int(dump_only=True)
    parent_id = fields.Int(dump_only=True)
    post_id = fields.Int(dump_only=True)
    created_time = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    points = fields.Nested(CommentPointSchema(), many=True)


class NestedCommentSchema(Schema):
    comment_id = fields.Int(dump_only=True)
    comment_text = fields.Str(required=True)
    user_id = fields.Int(dump_only=True)
    parent_id = fields.Int(dump_only=True)
    post_id = fields.Int(dump_only=True)
    created_time = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    points = fields.Nested(CommentPointSchema(), many=True)
    comments = fields.Nested(CommentSchema(), many=True)