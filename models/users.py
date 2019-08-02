from utils.extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import func


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
    roles = db.relationship("UserRolesModel", backref='users', lazy=True, cascade='delete')

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


class UserPointModel(db.Model):
    def __init__(self, user_id, points):
        self.user_id = user_id
        self.points = points

    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.user_id), unique=False, nullable=False)
    point_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    points = db.Column(db.Integer, nullable=False)
