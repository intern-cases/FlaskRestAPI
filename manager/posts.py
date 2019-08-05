from models.posts import PostModel, PostPointModel
from schemas.posts import PostSchema, PostPointSchema
from utils.extensions import db
posts_schema = PostSchema(many=True)


def get_posts_by_post_id(post_id):
    return PostModel.query.filter(post_id == PostModel.post_id).first()


def get_posts_by_user_id(user_id):
    return PostModel.query.filter(user_id == PostModel.user_id).first()


def get_all_posts_by_user_id(user_id):
    return PostModel.query.filter(user_id == PostModel.user_id).all()


def get_all_post():
    return PostModel.query.filter().all()


def db_commit():
    return db.session.commit()


def db_add(posts):
    return db.session.add(posts)


def db_delete(posts):
    return db.session.delete(posts)