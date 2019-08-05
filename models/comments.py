from utils.extensions import db
from datetime import datetime
from sqlalchemy.sql import func
from models.users import UserModel
from models.posts import PostModel


class CommentModel(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey(PostModel.post_id), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.user_id), nullable=False)
    parent_id = db.Column(db.Integer)
    comment_text = db.Column(db.String, nullable=False)
    created_time = db.Column(db.DateTime(timezone=True), default=func.now())
    points = db.relationship("CommentPointModel", backref='comments', cascade='delete')

    def __init__(self, user_id, post_id, comment_text, parent_id):
        self.comment_text = comment_text
        self.user_id = user_id
        self.post_id = post_id
        self.parent_id = parent_id
        self.created_time = datetime.utcnow()
        self.modified_at = datetime.utcnow()


class CommentPointModel(db.Model):
    def __init__(self, comment_id, points):
        self.comment_id = comment_id
        self.points = points

    comment_id = db.Column(db.Integer, db.ForeignKey(CommentModel.comment_id), unique=False, nullable=False)
    point_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    points = db.Column(db.Integer, nullable=False)
