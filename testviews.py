import flask

import authenticaton
from testalch import UserSchema, UserModel, PostSchema, PostModel, CommentSchema, CommentModel, UserPointModel, \
    UserPointSchema, PostPointModel, PostPointSchema, NestedCommentSchema, \
    CommentPointModel, CommentPointSchema, Manager, MigrateCommand, \
    db, app, UserRolesModel

manager = Manager(app)
manager.add_command('db', MigrateCommand)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

posts_schema = PostSchema(many=True)
comments_schema = CommentSchema(many=True)

user_points_schema = UserPointSchema(many=True)
post_points_schema = PostPointSchema(many=True)
comment_points_schema = CommentPointSchema(many=True)

"""""""""""""""""""""""""""""""""""USER TABLE ROUTES"""""""""""""""""""""""""""""""""""""""
"""
@app.route("/add_roles", methods=["POST"])
def add_roles():
    role_name = flask.request.json["role_name"]
    new_role = RoleModel(role_name)
    db.session.add(new_role)
    db.session.commit()
"""


@app.route("/set_roles", methods=["PUT"])
@authenticaton.login_required
def set_admin():
    user = UserRolesModel.query.filter(
        authenticaton.user_verifying == UserRolesModel.user_id).get(UserRolesModel.role_id)
    if user.role_id == 2:
        user_id = flask.request.json["user_id"]
        role_id = flask.request.json["role_id"]
        user = UserRolesModel.query.filter(user_id == UserRolesModel.user_id).first()
        user.role_id = role_id
        db.session.commit()
    else:
        return flask.jsonify("You're not allowed to do this")


@app.route("/user", methods=["POST"])
def add_user():
    username = flask.request.json['username']
    email = flask.request.json['email']
    password = flask.request.json['password']
    role_id = 1
    new_user = UserModel(username, email, password)

    if username is None or password is None or email is None:
        flask.abort(404)
    if UserModel.query.filter(username == UserModel.username or email == UserModel.email).first() is not None:
        flask.abort(404)

    db.session.add(new_user)
    db.session.commit()
    new_user_role = UserRolesModel(new_user.user_id, role_id)
    db.session.add(new_user_role)
    db.session.commit()

    return flask.jsonify("Request done.")


@app.route("/set_points/<string:username>", methods=["POST"])
@authenticaton.login_required
def point_to_user(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    if authenticaton.user_verifying() == user.user_id:
        return flask.jsonify("You can't set points to yourself.")
    else:
        points = flask.request.json["point"]
        if 0 <= int(points) <= 10:
            user_id = user.user_id
            point_user = UserPointModel(user_id, int(points))
            db.session.add(point_user)
            db.session.commit()
            return flask.jsonify(point_user)
        else:
            return flask.jsonify("You have to set points between 0 and 10.")


@app.route("/user_panel", methods=["GET"])
@authenticaton.login_required
def get_logged_user():
    spesific_user = UserModel.query.filter(authenticaton.user_verifying() == UserModel.user_id).first()
    result = user_schema.dump(spesific_user)
    return flask.jsonify(result.data)


@app.route("/users", methods=["GET"])
def get_users():
    all_users = UserModel.query.all()
    result = users_schema.dump(all_users)
    return flask.jsonify(result.data)


@app.route("/user/<int:user_id>", methods=["GET"])
def user_detail(user_id):
    user = UserModel.query.filter(user_id == UserModel.user_id).first()
    result = user_schema.dump(user)
    return flask.jsonify(result.data)


@app.route("/user/<string:username>", methods=["GET"])
def user_detail_by_username(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    result = user_schema.dump(user)
    return flask.jsonify(result.data)


@app.route("/user/<string:username>", methods=["PUT"])
@authenticaton.login_required
def user_update(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    if user.user_id == authenticaton.user_verifying() or authenticaton.is_admin(authenticaton.user_verifying()):
        username = flask.request.json['username']
        password = flask.request.json['password']
        email = flask.request.json['email']
        user.email = email
        user.username = username
        user.password_hash = password

        db.session.commit()
        return flask.jsonify(user)
    else:
        return flask.jsonify("You're not allowed to do this action.")


@app.route("/user/<int:user_id>", methods=["DELETE"])
@authenticaton.login_required
def user_delete(user_id):
    if user_id == authenticaton.user_verifying() or authenticaton.is_admin(authenticaton.user_verifying()):
        user = UserModel.query.filter(authenticaton.user_verifying() == UserModel.user_id).first()
        db.session.delete(user)
        db.session.commit()
        return flask.jsonify(user)
    else:
        return flask.jsonify("You're not allowed to do this action.")


@app.route("/user/<string:username>", methods=["DELETE"])
@authenticaton.login_required
def user_delete_by_username(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    if authenticaton.user_verifying() == user.user_id or authenticaton.is_admin(authenticaton.user_verifying()):
        db.session.delete(user)
        db.session.commit()
        return flask.jsonify(user)
    else:
        return flask.jsonify("You're not allowed to do this action.")


"""""""""""""""""""""""""""""""""""POST TABLE ROUTES"""""""""""""""""""""""""""""""""""""""""""""


@app.route("/post", methods=["POST"])
@authenticaton.login_required
def add_post():
    user_id = authenticaton.user_verifying()
    post_text = flask.request.json["post_text"]
    new_post = PostModel(post_text, user_id)
    db.session.add(new_post)
    db.session.commit()
    return flask.jsonify(new_post)


@app.route("/set_points_post/<int:post_id>", methods=["POST"])
@authenticaton.login_required
def points_to_post(post_id):
    post = PostModel.query.filter(post_id == PostModel.post_id).first()
    point = flask.request.json["point"]
    if authenticaton.user_verifying() == post.user_id:
        return flask.jsonify("You can't set points to your post.")
    else:
        if int(point) >= 0 or int(point) <= 10:
            user_id = authenticaton.user_verifying()
            point_post = PostPointModel(user_id, post_id, int(point))
            db.session.add(point_post)
            db.session.commit()
            return flask.jsonify(point_post)
        else:
            return flask.jsonify("You have to set points between 0 and 10.")


@app.route("/my_posts", methods=["GET"])
@authenticaton.login_required
def logged_users_post():
    my_post = PostModel.query.filter(PostModel.user_id == authenticaton.user_verifying())
    result = posts_schema.dump(my_post)
    return flask.jsonify(result.data)


@app.route("/main_page", methods=["GET"])
def get_posts():
    all_posts = PostModel.query.all()
    result = posts_schema.dump(all_posts)
    return flask.jsonify(result.data)



@app.route("/post/<int:user_id>", methods=["GET"])
def post_detail(user_id):
    posts = PostModel.query.filter(user_id == PostModel.user_id).all()
    result = posts_schema.dump(posts)
    return flask.jsonify(result.data)



@app.route("/post/<string:username>", methods=["GET"])
def post_detail_by_username(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    post = PostModel.query.filter(user.user_id == PostModel.user_id).all()
    result = posts_schema.dump(post)
    return flask.jsonify(result.data)


@app.route("/post/<int:user_id>/<int:post_id>", methods=["PUT"])
@authenticaton.login_required
def post_update(user_id, post_id):
    post = PostModel.query.filter(user_id == PostModel.user_id and post_id == PostModel.post_id).first()
    post_text = flask.request.json["post_text"]
    if authenticaton.user_verifying() == post.user_id or authenticaton.is_admin(authenticaton.user_verifying()):
        post.post_text = post_text

        db.session.commit()
        return flask.jsonify(post)

    else:
        return flask.jsonify("You're not allowed to do this.")


@app.route("/post/<int:post_id>", methods=["DELETE"])
@authenticaton.login_required
def post_delete(post_id):
    post = PostModel.query.filter(
        authenticaton.user_verifying() == PostModel.user_id and post_id == PostModel.post_id).first()
    if authenticaton.user_verifying() == post.user_id or authenticaton.is_admin(authenticaton.user_verifying()):
        db.session.delete(post)
        db.session.commit()
        return flask.jsonify(post)
    else:
        return flask.jsonify("You're not allowed to do this action.")


"""""""""""""""""""""""""""""""""""Comment table routes"""""""""""""""""""""""""""""""""""""""""""""


@app.route("/comment/post<int:post_id>", methods=["POST"])
@authenticaton.login_required
def add_comment_to_post(post_id):
    user_id = authenticaton.user_verifying()
    post = PostModel.query.filter(post_id == PostModel.post_id).first()
    comment_text = flask.request.json["comment_text"]
    parent_id = None
    new_comment = CommentModel(user_id, post.post_id, comment_text, parent_id)
    db.session.add(new_comment)
    db.session.commit()
    return flask.jsonify(new_comment)


@app.route("/comment/<int:comment_id>", methods=["POST"])
@authenticaton.login_required
def add_comment_to_comment(comment_id):
    user_id = authenticaton.user_verifying()
    post_id = PostModel.query.filter(user_id == PostModel.user_id).get(PostModel.post_id)
    parent_id = comment_id
    comment_text = flask.request.json["comment_text"]
    comment = CommentModel(user_id, post_id, comment_text, parent_id)
    db.session.add(comment)
    db.session.commit()
    return flask.jsonify("Request done.")


@app.route("/set_points_comment/<int:comment_id>", methods=["POST"])
@authenticaton.login_required
def points_to_comment(comment_id):
    comment = CommentModel.query.filter(comment_id == CommentModel.comment_id).first()
    if authenticaton.user_verifying() == comment.user_id:
        return flask.jsonify("You can't set points to your comment.")
    else:
        points = flask.request.json["points"]
        if 0 <= int(points) <= 10:
            user_id = authenticaton.user_verifying()
            post_id = comment.post_id
            comment_id = comment.comment_id
            point_comment = CommentPointModel(user_id, post_id, comment_id, int(points))
            db.session.add(point_comment)
            db.session.commit()
            return flask.jsonify(point_comment)
        else:
            return flask.jsonify("You have to set points between 0 and 10.")


@app.route("/post<int:post_id>/comments", methods=["GET"])
def get_comments_from_post(post_id):
    if CommentModel.query.order_by(post_id == CommentModel.post_id and CommentModel.parent_id is None).all():
        all_comments = CommentModel.query.order_by(post_id == CommentModel.post_id and CommentModel.parent_id is None).all()
        results = NestedCommentSchema.dump(all_comments)
        return flask.jsonify(results.data)
    else:
        all_comments = CommentModel.query.filter(post_id == CommentModel.post_id).all()
        results = CommentSchema.dump(all_comments)
        return flask.jsonify(results.data)


@app.route("/comment/<int:post_id>", methods=["PUT"])
@authenticaton.login_required
def posts_comment_update(post_id):
    post = CommentModel.query.filter(post_id == CommentModel.post_id).first()
    comment = CommentModel.query.filter(
        authenticaton.user_verifying() == CommentModel.user_id and CommentModel.post_id == post.post_id).first()
    if authenticaton.user_verifying() == comment.user_id or authenticaton.is_admin(authenticaton.user_verifying()):
        comment_text = flask.request.json["comment_text"]
        comment.comment_text = comment_text
        db.session.commit()
        return flask.jsonify(comment)
    else:
        return flask.jsonify("You're not allowed to do this action.")


@app.route("/comment/delete<int:comment_id>", methods=["DELETE"])
@authenticaton.login_required
def post_comment_delete(comment_id):
    comment = CommentModel.query.filter(comment_id == CommentModel.comment_id).first()
    if authenticaton.user_verifying() == comment.user_id or authenticaton.is_admin(authenticaton.user_verifying()):
        db.session.delete(comment)
        db.session.commit()
        return flask.jsonify(comment)
    else:
        return flask.jsonify("You're not allowed to do this action.")


if __name__ == '__main__':
    app.run(debug=True)
