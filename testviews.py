from flask import request, jsonify, abort

from authenticaton import user_verifying, login_required, is_admin
from testalch import UserSchema, UserModel, PostSchema, PostModel, CommentSchema, CommentModel, UserPointModel, \
    UserPointSchema, PostPointModel, PostPointSchema, CommentPointModel, CommentPointSchema, Manager, MigrateCommand, \
    db, app, UserRolesModel

manager = Manager(app)
manager.add_command('db', MigrateCommand)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

posts_schema = PostSchema(many=True)
comments_schema = CommentSchema(many=True)

userpoints_schema = UserPointSchema(many=True)
postpoints_schema = PostPointSchema(many=True)
commentpoints_schema = CommentPointSchema(many=True)

"""""""""""""""""""""""""""""""""""USER TABLE ROUTES"""""""""""""""""""""""""""""""""""""""""""""

""""@app.route("/addroles", methods=["POST"])
def add_roles():
    role_name = request.json["role_name"]
    new_role = RoleModel(role_name)
    db.session.add(new_role)
    db.session.commit()
"""


@app.route("/setroles", methods=["PUT"])
@login_required
def set_admin():
    user = UserRolesModel.query.filter(user_verifying == UserRolesModel.user_id).get(UserRolesModel.role_id)
    if user.role_id == 2:
        user_id = request.json["user_id"]
        role_id = request.json["role_id"]
        user = UserRolesModel.query.filter(user_id == UserRolesModel.user_id).first()
        user.role_id = role_id
        db.session.commit()
    else:
        return jsonify("You're not allowed to do this")


@app.route("/user", methods=["POST"])
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

    return jsonify(new_user)


@app.route("/set_points/<string:username>", methods=["POST"])
@login_required
def point_to_user(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    if user_verifying() == user.user_id:
        return jsonify("You can't set points to yourself.")
    else:
        point = request.json["point"]
        if 0 <= int(point) <= 10:
            user_id = user.user_id
            point_user = UserPointModel(user_id, int(point))
            db.session.add(point_user)
            db.session.commit()
            return jsonify(point_user)
        else:
            return jsonify("You have to set points between 0 and 10.")


@app.route("/user_panel", methods=["GET"])
@login_required
def get_logged_user():
    spesific_user = UserModel.query.filter(user_verifying() == UserModel.user_id).first()
    result = user_schema.dump(spesific_user)
    return jsonify(result.data)


@app.route("/users", methods=["GET"])
def get_users():
    all_users = UserModel.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


@app.route("/user/<int:user_id>", methods=["GET"])
def user_detail(user_id):
    user = UserModel.query.filter(user_id == UserModel.user_id).first()
    result = user_schema.dump(user)
    return jsonify(result.data)


@app.route("/user/<string:username>", methods=["GET"])
def user_detail_by_username(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    result = user_schema.dump(user)
    return jsonify(result.data)


@app.route("/user/<string:username>", methods=["PUT"])
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


@app.route("/user/<int:user_id>", methods=["DELETE"])
@login_required
def user_delete(user_id):
    if user_id == user_verifying() or is_admin(user_verifying()):
        user = UserModel.query.filter(user_verifying() == UserModel.user_id).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify(user)
    else:
        return jsonify("You're not allowed to do this action.")


@app.route("/user/<string:username>", methods=["DELETE"])
@login_required
def user_delete_by_username(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    if user_verifying() == user.user_id or is_admin(user_verifying()):
        db.session.delete(user)
        db.session.commit()
        return jsonify(user)
    else:
        return jsonify("You're not allowed to do this action.")


"""""""""""""""""""""""""""""""""""POST TABLE ROUTES"""""""""""""""""""""""""""""""""""""""""""""


@app.route("/post", methods=["POST"])
@login_required
def add_post():
    user_id = user_verifying()
    post_text = request.json["post_text"]
    new_post = PostModel(post_text, user_id)
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post)


@app.route("/set_points_post/<int:post_id>", methods=["POST"])
@login_required
def points_to_post(post_id):
    post = PostModel.query.filter(post_id == PostModel.post_id).first()
    if user_verifying() == post.user_id:
        return jsonify("You can't set points to your post.")
    else:
        point = request.json["point"]
        if 0 <= int(point) <= 10:
            user_id = post.user_id
            point_post = PostPointModel(user_id, int(point))
            db.session.add(point_post)
            db.session.commit()
            return jsonify(point_post)
        else:
            return jsonify("You have to set points between 0 and 10.")


@app.route("/my_posts", methods=["GET"])
@login_required
def logged_users_post():
    my_post = PostModel.query.filter(PostModel.user_id == user_verifying())
    result = posts_schema.dump(my_post)
    return jsonify(result.data)


@app.route("/main_page", methods=["GET"])
def get_posts():
    all_posts = PostModel.query.all()
    result = posts_schema.dump(all_posts)
    return jsonify(result.data)


@app.route("/post/<int:user_id>", methods=["GET"])
def post_detail(user_id):
    posts = PostModel.query.filter(user_id == PostModel.user_id).all()
    result = posts_schema.dump(posts)
    return jsonify(result.data)


@app.route("/post/<string:username>", methods=["GET"])
def post_detail_by_username(username):
    user = UserModel.query.filter(username == UserModel.username).first()
    post = PostModel.query.filter(user.user_id == PostModel.user_id).all()
    result = posts_schema.dump(post)
    return jsonify(result.data)


@app.route("/post/<int:user_id>/<int:post_id>", methods=["PUT"])
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


@app.route("/post/<int:post_id>", methods=["DELETE"])
@login_required
def post_delete(post_id):
    if user_verifying() == PostModel.user_id or is_admin(user_verifying()):
        post = PostModel.query.filter(user_verifying() == PostModel.user_id and post_id == PostModel.post_id).first()
        db.session.delete(post)
        db.session.commit()
        return jsonify(post)
    else:
        return jsonify("You're not allowed to do this action.")


"""""""""""""""""""""""""""""""""""Comment table routes"""""""""""""""""""""""""""""""""""""""""""""


@app.route("/comment/post<int:post_id>", methods=["POST"])
@login_required
def add_comment_to_post(post_id):
    user_id = user_verifying()
    post = PostModel.query.filter(post_id == PostModel.post_id).first()
    comment_text = request.json["comment_text"]
    new_comment = CommentModel(user_id, post.post_id, comment_text)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify(new_comment)


@app.route("/set_points_comment/<int:comment_id>", methods=["POST"])
@login_required
def points_to_comment(comment_id):
    comment = CommentModel.query.filter(comment_id == CommentModel.post_id).first()
    if user_verifying() == comment.user_id:
        return jsonify("You can't set points to your comment.")
    else:
        point = request.json["point"]
        if 0 <= int(point) <= 10:
            user_id = comment.user_id
            point_comment = CommentPointModel(user_id, int(point))
            db.session.add(point_comment)
            db.session.commit()
            return jsonify(point_comment)
        else:
            return jsonify("You have to set points between 0 and 10.")


@app.route("/post<int:post_id>/comments", methods=["GET"])
def get_comments_from_post(post_id):
    all_comments = CommentModel.query.order_by(post_id == CommentModel.post_id).all()
    results = comments_schema.dump(all_comments)
    return jsonify(results.data)


@app.route("/comment/<int:post_id>/<int:comment_id>", methods=["PUT"])
@login_required
def posts_comment_update(post_id, comment_id):
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


@app.route("/comment/delete<int:comment_id>", methods=["DELETE"])
@login_required
def post_comment_delete(comment_id):
    comment = CommentModel.query.filter(comment_id == CommentModel.comment_id).first()
    if user_verifying() == comment.user_id or is_admin(user_verifying()):
        db.session.delete(comment)
        db.session.commit()
        return jsonify(comment)
    else:
        return jsonify("You're not allowed to do this action.")


if __name__ == '__main__':
    app.run(debug=True)
