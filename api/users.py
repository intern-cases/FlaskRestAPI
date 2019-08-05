from flask import request, jsonify, abort, Blueprint
from models.users import UserPointModel, UserRolesModel
from schemas.users import UserPointSchema
from api.authentication import user_verifying, login_required, is_admin
from manager.users import *

user_points_schema = UserPointSchema(many=True)

blueprint_users = Blueprint("users", __name__, url_prefix='/users/')
""""@blueprint_users.route("/add_roles", methods=["POST"])
def add_roles():
    role_name = request.json["role_name"]
    new_role = RoleModel(role_name)
    db_add(new_role)
    db_commit()
    return jsonify("Role added.")"""


@blueprint_users.route("/set_roles", methods=["PUT"])
@login_required
def set_admin():
    if is_admin(user_verifying()):
        user_id = request.json["user_id"]
        role_id = request.json["role_id"]
        user = get_user_by_user_id(user_id)
        user.role_id = role_id
        db_commit()
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

    db_add(new_user)
    db_commit()
    new_user_role = UserRolesModel(new_user.user_id, role_id)
    db_add(new_user_role)
    db_commit()

    return jsonify("Request done.")


@blueprint_users.route("/set_points/<string:username>", methods=["POST"])
@login_required
def point_to_user(username):
    user = get_user_by_username(username)
    if user_verifying() == user.user_id:
        return jsonify("You can't set points to yourself.")
    else:
        points = request.json["point"]
        if 0 <= int(points) <= 10:
            user_id = user.user_id
            point_user = UserPointModel(user_id, int(points))
            db_add(point_user)
            db_commit()
            return jsonify(point_user)
        else:
            return jsonify("You have to set points between 0 and 10.")


@blueprint_users.route("/user_panel", methods=["GET"])
@login_required
def get_logged_user():
    spesific_user = get_user_by_user_id(user_verifying())
    result = user_schema.dump(spesific_user)
    return jsonify(result.data)


@blueprint_users.route("/list", methods=["GET"])
def get_users():
    all_users = get_all_user()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


@blueprint_users.route("/<int:user_id>", methods=["GET"])
def user_detail(user_id):
    user = get_user_by_user_id(user_id)
    result = user_schema.dump(user)
    return jsonify(result.data)


@blueprint_users.route("/<string:username>", methods=["GET"])
def user_detail_by_username(username):
    user = get_user_by_username(username)
    result = user_schema.dump(user)
    return jsonify(result.data)


@blueprint_users.route("/<string:username>", methods=["PUT"])
@login_required
def user_update(username):
    user = get_user_by_username(username)
    if user.user_id == user_verifying() or is_admin(user_verifying()):
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        user.email = email
        user.username = username
        user.password_hash = password

        db_commit()
        return jsonify(user)
    else:
        return jsonify("You're not allowed to do this action.")


@blueprint_users.route("/delete/<int:user_id>", methods=["DELETE"])
@login_required
def user_delete(user_id):
    if user_id == user_verifying() or is_admin(user_verifying()):
        user = get_user_by_user_id(user_verifying())
        db_delete(user)
        db_commit()
        return jsonify(user)
    else:
        return jsonify("You're not allowed to do this action.")


@blueprint_users.route("/delete/<string:username>", methods=["DELETE"])
@login_required
def user_delete_by_username(username):
    user = get_user_by_username(username)
    if user_verifying() == user.user_id or is_admin(user_verifying()):
        db_delete(user)
        db_commit()
        return jsonify(user)
    else:
        return jsonify("You're not allowed to do this action.")
