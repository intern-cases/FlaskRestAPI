from datetime import datetime
from models.users import UserModel
from utils.extensions import db
from sqlalchemy.sql import func



class PostModel(db.Model):
    post_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.user_id), nullable=False)
    post_text = db.Column(db.String, nullable=False)
    comments = db.relationship("CommentModel", backref='posts', cascade='delete')
    created_time = db.Column(db.DateTime(timezone=True), default=func.now())
    points = db.relationship("PostPointModel", backref='posts', cascade='delete')

    def __init__(self, post_text, user_id):
        self.user_id = user_id
        self.post_text = post_text
        self.created_time = datetime.utcnow()
        self.modified_at = datetime.utcnow()

    def __repr__(self):
        return '<Post %r>' % self.post_text


class PostPointModel(db.Model):
    def __init__(self, user_id, post_id, points):
        self.user_id = user_id
        self.post_id = post_id
        self.points = points

    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.user_id), unique=False, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(PostModel.post_id), unique=False, nullable=False)
    point_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    points = db.Column(db.Integer, nullable=False)



