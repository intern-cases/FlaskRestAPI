from flask import request, jsonify, abort, Blueprint
from models.users import UserPointModel, UserRolesModel, UserModel
from utils.extensions import db
from schemas.users import UserPointSchema, UserSchema
from api.authentication import user_verifying, login_required, is_admin

user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_points_schema = UserPointSchema(many=True)

"""
@app.route("/add_roles", methods=["POST"])
def add_roles():
    role_name = flask.request.json["role_name"]
    new_role = RoleModel(role_name)
    db.session.add(new_role)
    db.session.commit()
"""
blueprint_users = Blueprint("users", __name__, url_prefix='/users/')


@blueprint_users.route("/set_roles", methods=["PUT"])
@login_required
def set_admin():
    user = UserRolesModel.query.filter(
        user_verifying == UserRolesModel.user_id).get(UserRolesModel.role_id)
    if user.role_id == 2:
        user_id = request.json["user_id"]
        role_id = request.json["role_id"]
        user = UserRolesModel.query.filter(user_id == UserRolesModel.user_id).first()
        user.role_id = role_id
        db.session.commit()
    else:
        return jsonify("You're not allowed to do this")


@blueprint_users.route("/sign_up", methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    role_id = 1
    new_user = UserModel(username, email, password)

    if username is None or password is None or email is None:
        abort(404)
    if UserModel.query.filter(username == UserModel.username or email == UserModel.email).first() is not None:
        abort(404)

    db.session.add(new_user)
    db.session.commit()
    new_user_role = UserRolesModel(new_user.user_id, role_id)
    db.session.add(new_user_role)
    db.session.commit()

    return jsonify("Request done.")


@blueprint_users.route("/set_points/<string:username>", methods=["POST"])
@login_required
def point_to_user(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    if user_verifying() == user.user_id:
        return jsonify("You can't set points to yourself.")
    else:
        points = request.json["point"]
        if 0 <= int(points) <= 10:
            user_id = user.user_id
            point_user = UserPointModel(user_id, int(points))
            db.session.add(point_user)
            db.session.commit()
            return jsonify(point_user)
        else:
            return jsonify("You have to set points between 0 and 10.")


@blueprint_users.route("/user_panel", methods=["GET"])
@login_required
def get_logged_user():
    spesific_user = UserModel.query.filter(user_verifying() == UserModel.user_id).first()
    result = user_schema.dump(spesific_user)
    return jsonify(result.data)


@blueprint_users.route("/list", methods=["GET"])
def get_users():
    all_users = UserModel.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


@blueprint_users.route("/<int:user_id>", methods=["GET"])
def user_detail(user_id):
    user = UserModel.query.filter(user_id == UserModel.user_id).first()
    result = user_schema.dump(user)
    return jsonify(result.data)


@blueprint_users.route("/<string:username>", methods=["GET"])
def user_detail_by_username(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    result = user_schema.dump(user)
    return jsonify(result.data)


@blueprint_users.route("/<string:username>", methods=["PUT"])
@login_required
def user_update(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    if user.user_id == user_verifying() or is_admin(user_verifying()):
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        user.email = email
        user.username = username
        user.password_hash = password

        db.session.commit()
        return jsonify(user)
    else:
        return jsonify("You're not allowed to do this action.")


@blueprint_users.route("/<int:user_id>", methods=["DELETE"])
@login_required
def user_delete(user_id):
    if user_id == user_verifying() or is_admin(user_verifying()):
        user = UserModel.query.filter(user_verifying() == UserModel.user_id).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify(user)
    else:
        return jsonify("You're not allowed to do this action.")


@blueprint_users.route("/delete/<string:username>", methods=["DELETE"])
@login_required
def user_delete_by_username(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    if user_verifying() == user.user_id or is_admin(user_verifying()):
        db.session.delete(user)
        db.session.commit()
        return jsonify(user)
    else:
        return jsonify("You're not allowed to do this action.")
