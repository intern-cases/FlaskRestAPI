from flask import request, jsonify, Blueprint
from models.comments import CommentPointModel
from manager.comments import *
from manager.posts import *
from api.authentication import user_verifying, login_required, is_admin

comments_schema = CommentSchema(many=True)
nested_schema = NestedCommentSchema(many=True)

blueprint_comments = Blueprint("comments", __name__, url_prefix='/comments/')


@blueprint_comments.route("/post<int:post_id>", methods=["POST"])
@login_required
def add_comment_to_post(post_id):
    user_id = user_verifying()
    post = get_posts_by_post_id(post_id)
    comment_text = request.json["comment_text"]
    parent_id = None
    new_comment = CommentModel(user_id, post.post_id, comment_text, parent_id)
    db_add(new_comment)
    db_commit()
    return jsonify(new_comment)


@blueprint_comments.route("/<int:comment_id>", methods=["POST"])
@login_required
def add_comment_to_comment(comment_id):
    user_id = user_verifying()
    post = get_posts_by_user_id(user_id)
    post_id = post.post_id
    parent_id = comment_id
    comment_text = request.json["comment_text"]
    comment = CommentModel(user_id, post_id, comment_text, parent_id)
    db_add(comment)
    db_commit()
    return jsonify("Request done.")


@blueprint_comments.route("/set_points_comment/<int:comment_id>", methods=["POST"])
@login_required
def points_to_comment(comment_id):
    comment = get_comment_by_comment_id(comment_id)
    if user_verifying() == comment.user_id:
        return jsonify("You can't set points to your comment.")
    else:
        points = request.json["points"]
        if 0 <= int(points) <= 10:
            user_id = user_verifying()
            post_id = comment.post_id
            comment_id = comment.comment_id
            point_comment = CommentPointModel(user_id, post_id, comment_id, int(points))

            db_commit()
            return jsonify(point_comment)
        else:
            return jsonify("You have to set points between 0 and 10.")


@blueprint_comments.route("/post<int:post_id>", methods=["GET"])
def get_comments_from_post(post_id):
    if get_posts_comments(post_id):
        all_comments = get_posts_comments(post_id)
        results = NestedCommentSchema.dump(all_comments)
        return jsonify(results.data)
    else:
        all_comments = get_all_comment(post_id)
        results = CommentSchema.dump(all_comments)
        return jsonify(results.data)


@blueprint_comments.route("/<int:post_id>", methods=["PUT"])
@login_required
def posts_comment_update(post_id):
    post = get_one_comment(post_id)
    comment = get_spesific_comment(user_verifying(), post)
    if user_verifying() == comment.user_id or is_admin(user_verifying()):
        comment_text = request.json["comment_text"]
        comment.comment_text = comment_text
        db_commit()
        return jsonify(comment)
    else:
        return jsonify("You're not allowed to do this action.")


@blueprint_comments.route("/delete<int:comment_id>", methods=["DELETE"])
@login_required
def post_comment_delete(comment_id):
    comment = get_comment_by_comment_id(comment_id)
    if user_verifying() == comment.user_id or is_admin(user_verifying()):
        db_delete(comment)
        db_commit()
        return jsonify(comment)
    else:
        return jsonify("You're not allowed to do this action.")
