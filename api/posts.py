from flask import request, jsonify, Blueprint
from api.authentication import user_verifying, login_required, is_admin
from manager.posts import *
from manager.users import get_user_by_username


blueprint_posts = Blueprint("posts", __name__, url_prefix='/posts/')


@blueprint_posts.route("/post", methods=["POST"])
@login_required
def add_post():
    user_id = user_verifying()
    post_text = request.json["post_text"]
    new_post = PostModel(post_text, user_id)
    db_add(new_post)
    db_commit()
    return jsonify(new_post)


@blueprint_posts.route("/set_points_post/<int:post_id>", methods=["POST"])
@login_required
def points_to_post(post_id):
    post = get_posts_by_post_id(post_id)
    point = request.json["point"]
    if user_verifying() == post.user_id:
        return jsonify("You can't set points to your post.")
    else:
        if int(point) >= 0 or int(point) <= 10:
            user_id = user_verifying()
            point_post = PostPointModel(user_id, post_id, int(point))
            db_add(point_post)
            db_commit()
            return jsonify(point_post)
        else:
            return jsonify("You have to set points between 0 and 10.")


@blueprint_posts.route("/my_posts", methods=["GET"])
@login_required
def logged_users_post():
    my_post = get_posts_by_user_id(user_verifying())
    result = posts_schema.dump(my_post)
    return jsonify(result.data)


@blueprint_posts.route("/main_page", methods=["GET"])
def get_posts():
    all_posts = get_all_post()
    result = posts_schema.dump(all_posts)
    return jsonify(result.data)


@blueprint_posts.route("/<int:user_id>", methods=["GET"])
def post_detail(user_id):
    posts = PostModel.query.filter(user_id == PostModel.user_id).all()
    result = posts_schema.dump(posts)
    return jsonify(result.data)


@blueprint_posts.route("/<string:username>", methods=["GET"])
def post_detail_by_username(username):
    user = get_user_by_username(username)
    post = get_all_posts_by_user_id(user.user_id)
    result = posts_schema.dump(post)
    return jsonify(result.data)


@blueprint_posts.route("/<int:user_id>/<int:post_id>", methods=["PUT"])
@login_required
def post_update(user_id, post_id):
    post = PostModel.query.filter(user_id == PostModel.user_id and post_id == PostModel.post_id).first()
    post_text = request.json["post_text"]
    if user_verifying() == post.user_id or is_admin(user_verifying()):
        post.post_text = post_text

        db_commit()
        return jsonify(post)

    else:
        return jsonify("You're not allowed to do this.")


@blueprint_posts.route("/<int:post_id>", methods=["DELETE"])
@login_required
def post_delete(post_id):
    post = PostModel.query.filter(
        user_verifying() == PostModel.user_id and post_id == PostModel.post_id).first()
    if user_verifying() == post.user_id or is_admin(user_verifying()):
        db_delete(post)
        db_commit()
        return jsonify(post)
    else:
        return jsonify("You're not allowed to do this action.")