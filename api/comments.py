from flask import request, jsonify, Blueprint
from models.comments import CommentModel, CommentPointModel
from models.posts import PostModel
from schemas.comments import CommentSchema, CommentPointSchema, NestedCommentSchema

from utils.extensions import db
from api.authentication import user_verifying, login_required, is_admin

comments_schema = CommentSchema(many=True)
comment_points_schema = CommentPointSchema(many=True)


blueprint_comments = Blueprint("comments", __name__, url_prefix='/comments/')


@blueprint_comments.route("/comment/post<int:post_id>", methods=["POST"])
@login_required
def add_comment_to_post(post_id):
    user_id = user_verifying()
    post = PostModel.query.filter(post_id == PostModel.post_id).first()
    comment_text = request.json["comment_text"]
    parent_id = None
    new_comment = CommentModel(user_id, post.post_id, comment_text, parent_id)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify(new_comment)


@blueprint_comments.route("/comment/<int:comment_id>", methods=["POST"])
@login_required
def add_comment_to_comment(comment_id):
    user_id = user_verifying()
    post_id = PostModel.query.filter(user_id == PostModel.user_id).get(PostModel.post_id)
    parent_id = comment_id
    comment_text = request.json["comment_text"]
    comment = CommentModel(user_id, post_id, comment_text, parent_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify("Request done.")


@blueprint_comments.route("/set_points_comment/<int:comment_id>", methods=["POST"])
@login_required
def points_to_comment(comment_id):
    comment = CommentModel.query.filter(comment_id == CommentModel.comment_id).first()
    if user_verifying() == comment.user_id:
        return jsonify("You can't set points to your comment.")
    else:
        points = request.json["points"]
        if 0 <= int(points) <= 10:
            user_id = user_verifying()
            post_id = comment.post_id
            comment_id = comment.comment_id
            point_comment = CommentPointModel(user_id, post_id, comment_id, int(points))
            db.session.add(point_comment)
            db.session.commit()
            return jsonify(point_comment)
        else:
            return jsonify("You have to set points between 0 and 10.")


@blueprint_comments.route("/post<int:post_id>/comments", methods=["GET"])
def get_comments_from_post(post_id):
    if CommentModel.query.order_by(post_id == CommentModel.post_id and CommentModel.parent_id is None).all():
        all_comments = CommentModel.query.order_by(post_id == CommentModel.post_id and CommentModel.parent_id is None).all()
        results = NestedCommentSchema.dump(all_comments)
        return jsonify(results.data)
    else:
        all_comments = CommentModel.query.filter(post_id == CommentModel.post_id).all()
        results = CommentSchema.dump(all_comments)
        return jsonify(results.data)


@blueprint_comments.route("/comment/<int:post_id>", methods=["PUT"])
@login_required
def posts_comment_update(post_id):
    post = CommentModel.query.filter(post_id == CommentModel.post_id).first()
    comment = CommentModel.query.filter(
        user_verifying() == CommentModel.user_id and CommentModel.post_id == post.post_id).first()
    if user_verifying() == comment.user_id or is_admin(user_verifying()):
        comment_text = request.json["comment_text"]
        comment.comment_text = comment_text
        db.session.commit()
        return jsonify(comment)
    else:
        return jsonify("You're not allowed to do this action.")


@blueprint_comments.route("/comment/delete<int:comment_id>", methods=["DELETE"])
@login_required
def post_comment_delete(comment_id):
    comment = CommentModel.query.filter(comment_id == CommentModel.comment_id).first()
    if user_verifying() == comment.user_id or is_admin(user_verifying()):
        db.session.delete(comment)
        db.session.commit()
        return jsonify(comment)
    else:
        return jsonify("You're not allowed to do this action.")

