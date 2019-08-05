from models.comments import CommentModel
from utils.extensions import db
from schemas.comments import CommentSchema, NestedCommentSchema

comments_schema = CommentSchema(many=True)
nested_schema = NestedCommentSchema(many=True)


def get_comment_by_comment_id(comment_id):
    return CommentModel.query.filter(comment_id == CommentModel.comment_id).first()


def get_posts_comments(post_id):
    return CommentModel.query.order_by(post_id == CommentModel.post_id and CommentModel.parent_id is None).all()


def get_all_comment(post_id):
    return CommentModel.query.filter(post_id == CommentModel.post_id).all()


def get_one_comment(post_id):
    return CommentModel.query.filter(post_id == CommentModel.post_id).first()


def get_spesific_comment(user_id, post):
    CommentModel.query.filter(
        user_id == CommentModel.user_id and CommentModel.post_id == post.post_id).first()


def db_commit():
    return db.session.commit()


def db_add(comment):
    return db.session.add(comment)


def db_delete(comment):
    return db.session.delete(comment)


def dump_comment(all_comments):
    return comments_schema.dump(all_comments)


def dump_nested(all_comments):
    return nested_schema.dump(all_comments)