from flask import request, jsonify, Blueprint
from models.users import UserModel
from schemas.posts import PostSchema, PostPointSchema
from models.posts import PostModel, PostPointModel
from utils.extensions import db
from authentication import user_verifying, login_required, is_admin

posts_schema = PostSchema(many=True)
post_points_schema = PostPointSchema(many=True)

blueprint_posts = Blueprint("posts", __name__, url_prefix='/posts/')


@blueprint_posts.route("/post", methods=["POST"])
@login_required
def add_post():
    user_id = user_verifying()
    post_text = request.json["post_text"]
    new_post = PostModel(post_text, user_id)
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post)


@blueprint_posts.route("/set_points_post/<int:post_id>", methods=["POST"])
@login_required
def points_to_post(post_id):
    post = PostModel.query.filter(post_id == PostModel.post_id).first()
    point = request.json["point"]
    if user_verifying() == post.user_id:
        return jsonify("You can't set points to your post.")
    else:
        if int(point) >= 0 or int(point) <= 10:
            user_id = user_verifying()
            point_post = PostPointModel(user_id, post_id, int(point))
            db.session.add(point_post)
            db.session.commit()
            return jsonify(point_post)
        else:
            return jsonify("You have to set points between 0 and 10.")


@blueprint_posts.route("/my_posts", methods=["GET"])
@login_required
def logged_users_post():
    my_post = PostModel.query.filter(PostModel.user_id == user_verifying())
    result = posts_schema.dump(my_post)
    return jsonify(result.data)


@blueprint_posts.route("/main_page", methods=["GET"])
def get_posts():
    all_posts = PostModel.query.all()
    result = posts_schema.dump(all_posts)
    return jsonify(result.data)


@blueprint_posts.route("/post/<int:user_id>", methods=["GET"])
def post_detail(user_id):
    posts = PostModel.query.filter(user_id == PostModel.user_id).all()
    result = posts_schema.dump(posts)
    return jsonify(result.data)


@blueprint_posts.route("/post/<string:username>", methods=["GET"])
def post_detail_by_username(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    post = PostModel.query.filter(user.user_id == PostModel.user_id).all()
    result = posts_schema.dump(post)
    return jsonify(result.data)


@blueprint_posts.route("/post/<int:user_id>/<int:post_id>", methods=["PUT"])
@login_required
def post_update(user_id, post_id):
    post = PostModel.query.filter(user_id == PostModel.user_id and post_id == PostModel.post_id).first()
    post_text = request.json["post_text"]
    if user_verifying() == post.user_id or is_admin(user_verifying()):
        post.post_text = post_text

        db.session.commit()
        return jsonify(post)

    else:
        return jsonify("You're not allowed to do this.")


@blueprint_posts.route("/post/<int:post_id>", methods=["DELETE"])
@login_required
def post_delete(post_id):
    post = PostModel.query.filter(
        user_verifying() == PostModel.user_id and post_id == PostModel.post_id).first()
    if user_verifying() == post.user_id or is_admin(user_verifying()):
        db.session.delete(post)
        db.session.commit()
        return jsonify(post)
    else:
        return jsonify("You're not allowed to do this action.")