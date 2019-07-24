from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash
from flask_script import Manager
from sqlalchemy.sql import func
import datetime
from marshmallow import fields, Schema, validate

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://omerfarukaslandogdu:Wasbornaslion1?@localhost:5432/testcase'

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class RoleModel(db.Model):
    role_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(), unique=True)
    users = db.relationship("UserRolesModel", backref='roles', cascade='delete', lazy=True)

    def __init__(self, role_name):
        self.role_name = role_name


class UserModel(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String(120), unique=True, nullable=False)
    created_time = db.Column(db.DateTime(timezone=True), default=func.now())
    modified_at = db.Column(db.DateTime(timezone=True), default=func.now())
    comments = db.relationship('CommentModel', backref='users', cascade='delete', lazy=True)
    posts = db.relationship('PostModel', backref='users', cascade='delete', lazy=True)
    points = db.relationship("UserPointModel", backref='users', cascade='delete', lazy=True)
    roles = db.relationship("UserRolesModel", backref='users', lazy=True)

    def __init__(self, username, email, raw_password):
        self.username = username
        self.email = email
        # Save the hashed password
        self.set_password(raw_password)

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserRolesModel(db.Model):
    user_role_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(UserModel.user_id), unique=True)
    role_id = db.Column(db.Integer(), db.ForeignKey(RoleModel.role_id))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id


class PostModel(db.Model):
    post_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.user_id), nullable=False)
    post_text = db.Column(db.String, nullable=False)
    comments = db.relationship("CommentModel", backref='posts', cascade='delete', lazy=True)
    created_time = db.Column(db.DateTime(timezone=True), default=func.now())
    points = db.relationship("PostPointModel", backref='posts', cascade='delete', lazy=True)

    def __init__(self, post_text, user_id):
        self.user_id=user_id
        self.post_text = post_text
        self.created_time = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def __repr__(self):
        return '<Post %r>' % self.post_text


class CommentModel(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey(PostModel.post_id), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.user_id), nullable=False)
    parent_id = db.Column(db.Integer)
    comment_text = db.Column(db.String, nullable=False)
    created_time = db.Column(db.DateTime(timezone=True), default=func.now())
    points = db.relationship("CommentPointModel", backref='comments', cascade='delete', lazy=True)
    #   comments = db.relationship("t_comment", backref='comments', cascade = 'delete', lazy=True)

    def __init__(self, user_id, post_id, comment_text):
        self.comment_text = comment_text
        self.user_id = user_id
        self.post_id = post_id
        self.created_time = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()


"""""""""""""""""""""""""""""""Point Model"""""""""""""""""""""""""""""""""""""""""""


class UserPointModel(db.Model):

    def __init__(self, user_id, points):
        self.user_id = user_id
        self.points = points

    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.user_id), unique=False, nullable=False)
    point_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    points = db.Column(db.Integer, nullable=False)


class PostPointModel(db.Model):

    def __init__(self, post_id, points):
        self.post_id = post_id
        self.points = points

    post_id = db.Column(db.Integer, db.ForeignKey(PostModel.post_id), unique=False, nullable=False)
    point_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    points = db.Column(db.Integer, nullable=False)


class CommentPointModel(db.Model):

    def __init__(self, comment_id, points):
        self.comment_id = comment_id
        self.points = points

    comment_id = db.Column(db.Integer, db.ForeignKey(CommentModel.comment_id), unique=False, nullable=False)
    point_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    points = db.Column(db.Integer, nullable=False)


""""""""""""""""""""""""""""""""""Schemalar"""""""""""""""""""""""""""""""""""""""""""""""""""""


class UserPointSchema(Schema):
    user_id = fields.Int(dump_only=True)
    point_id = fields.Int(dump_only=True, autoincrement=True)
    points = fields.Int(validate=validate.Range(min=0, max=10))


class PostPointSchema(Schema):
    post_id = fields.Int(dump_only=True)
    point_id = fields.Int(dump_only=True, autoincrement=True)
    points = fields.Int(validate=validate.Range(min=0, max=10))


class CommentPointSchema(Schema):
    comment_id = fields.Int(dump_only=True)
    point_id = fields.Int(dump_only=True, autoincrement=True)
    points = fields.Int(validate=validate.Range(min=0, max=10))


# comment şeması
class CommentSchema(Schema):
    comment_id = fields.Int(dump_only=True)
    comment_text = fields.Str(required=True)
    user_id = fields.Int(dump_only=True)
    parent_id = fields.Int(dump_only=True)
    post_id = fields.Int(dump_only=True)
    created_time = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    points = fields.Nested(CommentPointSchema(), many=True)
    #comments = fields.Nested(CommentSchema(), many=True)


# post şeması
class PostSchema(Schema):
    comments = fields.Nested(CommentSchema(), many=True)
    modified_at = fields.DateTime(dump_only=True)
    created_time = fields.DateTime(dump_only=True)
    user_id = fields.Int(required=True)
    post_text = fields.Str(required=True)
    post_id = fields.Int(dump_only=True)
    points = fields.Nested(PostPointSchema(), many=True)


# kullanıcı şeması
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


db.session.commit()

if __name__ == '__main__':
    manager.run()
